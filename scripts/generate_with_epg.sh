#!/bin/bash

# IPTV + EPG 自动集成脚本
# 功能：每天自动下载 IPTV 和 EPG，合并生成完整订阅包

set -e

# ================= 配置区 =================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 输出目录
OUTPUT_DIR="$PROJECT_ROOT"

# IPTV 源地址（仅在本地文件缺失时作为兜底）
IPTV_URL="https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv.m3u"

# EPG 源地址（国内推荐）
EPG_URL="http://epg.51zmt.top:8000/e.xml"
EPG_BACKUP="http://epg.pw/xmltv/epg.xml"

# 输出文件
M3U_FILE="$OUTPUT_DIR/iptv.m3u"
EPG_XML="$OUTPUT_DIR/epg.xml"
FULL_M3U="$OUTPUT_DIR/iptv-with-epg.m3u"

# 日志文件
LOG_FILE="$PROJECT_ROOT/logs/generate.log"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$PROJECT_ROOT/logs"

# ================= 函数定义 =================

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$LOG_FILE"
}

download_file() {
    local url=$1
    local output=$2
    local timeout=${3:-30}
    
    log "下载：$url"
    
    if command -v curl &>/dev/null; then
        if curl -sfL --connect-timeout "$timeout" "$url" -o "$output"; then
            log "✅ 下载成功：$url"
            return 0
        fi
    elif command -v wget &>/dev/null; then
        if wget -q --timeout="$timeout" "$url" -O "$output"; then
            log "✅ 下载成功：$url"
            return 0
        fi
    fi
    
    log "❌ 下载失败：$url"
    return 1
}

merge_iptv_with_epg() {
    local m3u=$1
    local epg_url=$2
    local output=$3
    
    log "正在合并 IPTV 与 EPG..."
    
    # 方法 1：在 M3U 头部添加 EPG URL
    {
        echo "#EXTM3U x-tvg-url=\"$epg_url\""
        echo "# 说明：本订阅已集成电子节目单 (EPG)，无需额外配置"
        echo "# EPG 源：$epg_url"
        echo "# 更新时间：$(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        
        # 读取原始 M3U 内容（跳过可能的第一行声明）
        tail -n +2 "$m3u"
    } > "$output"
    
    log "✅ 合并完成：$output"
}

verify_files() {
    local file=$1
    local min_lines=${2:-10}
    
    if [ ! -f "$file" ]; then
        log "❌ 文件不存在：$file"
        return 1
    fi
    
    local lines=$(wc -l < "$file")
    if [ "$lines" -lt "$min_lines" ]; then
        log "⚠️ 警告：$file 只有 $lines 行，可能异常"
        return 1
    fi
    
    log "✅ 文件验证通过：$file ($lines 行)"
    return 0
}

check_source_status() {
    log "检查 IPTV 源状态..."

    # 优先使用本地刚生成的 IPTV 文件，避免被远端旧版本覆盖
    if [ -f "$M3U_FILE" ] && verify_files "$M3U_FILE" 100; then
        log "✅ 使用本地 IPTV 文件：$M3U_FILE"
    else
        log "⚠️ 本地 IPTV 文件缺失或异常，尝试从远端兜底下载"
        if download_file "$IPTV_URL" "$M3U_FILE.tmp" 60; then
            verify_files "$M3U_FILE.tmp" 100
            mv "$M3U_FILE.tmp" "$M3U_FILE"
        else
            log "❌ IPTV 源获取失败，且本地文件不可用"
            rm -f "$M3U_FILE.tmp"
            return 1
        fi
    fi
    
    log "检查 EPG 源状态..."
    
    # 尝试下载主 EPG
    if download_file "$EPG_URL" "$EPG_XML" 60; then
        verify_files "$EPG_XML" 10
    else
        # 尝试备用 EPG
        log "尝试备用 EPG 源..."
        if download_file "$EPG_BACKUP" "$EPG_XML" 60; then
            verify_files "$EPG_XML" 10
        else
            log "⚠️ EPG 源均失败，跳过 EPG 部分"
            rm -f "$EPG_XML"
        fi
    fi
}

generate_output() {
    log "生成最终订阅文件..."
    
    # 如果没有 EPG 文件，使用默认 EPG URL
    local epg_url=$EPG_URL
    if [ ! -f "$EPG_XML" ]; then
        log "⚠️ 无本地 EPG 文件，将在 M3U 中保留外部 EPG URL"
        epg_url=$EPG_URL
    fi
    
    merge_iptv_with_epg "$M3U_FILE" "$epg_url" "$FULL_M3U"
    
    log "=========================="
    log "📊 文件统计"
    log "=========================="
    log "IPTV 频道数：$(grep -c "^#EXTINF:" "$M3U_FILE" 2>/dev/null || echo 0) 个"
    log "EPG 条目数：$(grep -c "<channel" "$EPG_XML" 2>/dev/null || echo 0) 个"
    log "生成时间：$(date '+%Y-%m-%d %H:%M:%S')"
}

main() {
    log "========================================"
    log "🔄 IPTV + EPG 自动更新开始"
    log "========================================"
    
    check_source_status
    
    generate_output
    
    log "========================================"
    log "✅ IPTV + EPG 自动更新完成"
    log "========================================"
    log ""
    log "📂 输出文件:"
    log "   - 纯 M3U:   $M3U_FILE"
    log "   - EPG 版 M3U: $FULL_M3U"
    log "   - EPG XML:  $EPG_XML"
    log ""
}

main
