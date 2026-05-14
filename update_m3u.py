#!/usr/bin/env python3
"""IPTV m3u 更新脚本：过滤分组、聚合线路、测试 IPv6 超时、重新排序"""

import re
import subprocess
import json
import time
import sys
from collections import defaultdict
from urllib.parse import urlparse

# 配置
VALID_GROUPS = ["央视频道", "卫视频道", "地方频道"]
FILTER_KEYWORDS = ["bdstatic.com", "支持作者", "轮播", "电影视界", "影视", "电影", "电视剧", 
                   "棋牌", "游戏", "卡通", "动漫", "体育", "ABC", "教学", "教育", "学习"]

def read_m3u(filepath):
    """读取 m3u 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def parse_m3u(content):
    """解析 m3u 为频道列表"""
    channels = defaultdict(list)
    current_channel = None
    current_group = None
    
    lines = content.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('#EXTINF:'):
            # 解析频道信息
            group_match = re.search(r'group-title="([^"]*)"', line)
            name_match = re.search(r',(.+)$', line)
            
            group = group_match.group(1) if group_match else ""
            name = name_match.group(1).strip() if name_match else ""
            
            current_channel = name
            current_group = group
            i += 1
            continue
            
        elif line and not line.startswith('#'):
            # 这是 URL 行
            if current_channel and current_group:
                channels[(current_group, current_channel)].append(line)
                # 重置，以便下一行可以开始新频道
                current_channel = None
                
        i += 1
    
    return channels

def filter_channel(name, group):
    """过滤掉非电视台频道"""
    # 核心央视频道和卫视频道应该保留
    if group == "央视频道":
        if "CCTV" in name or "CGTN" in name:
            return True
    
    if group == "卫视频道":
        # 卫视通常包含省份名 + 卫视/新闻/都市等
        if any(x in name for x in ["卫视", "新闻", "都市", "经济", "影视", "生活", 
                                   "公共", "教育", "少儿", "音乐", "体育", "国际"]):
            return True
    
    if group == "地方频道":
        # 地方频道：包含地名 + 新闻/综合/教育等
        # 排除明显的非电视台内容
        name_lower = name.lower()
        filtered_keywords = ["棋牌", "游戏", "电影视界", "影视", "棋牌游戏"]
        if any(kw in name_lower for kw in filtered_keywords):
            return False
        return True  # 保留地方频道，再把不合适的过滤掉
    
    return False

def is_ipv6_url(url):
    """检查是否为 IPv6 URL"""
    return '[2000:' in url.lower() or '[240' in url.lower()

def is_ipv4_url(url):
    """检查是否为 IPv4 URL"""
    ipv4_pattern = r'http[s]?://(?:[0-9]{1,3}\.){3}[0-9]{1,3}'
    return bool(re.search(ipv4_pattern, url))

def is_rtp(url):
    """检查是否为 rtp 协议 (通常是 IPv4)"""
    return url.startswith('rtp://')

def test_url_timeout(url, timeout=5):
    """测试 URL 是否能在超时时间内响应（仅用于 IPv6）"""
    # 如果无法通过 curl 测试，直接返回 False，不影响流程
    try:
        result = subprocess.run(
            ['curl', '-I', '-m', str(timeout), '-o', '/dev/null', '-s', '-w', '%{http_code}', url],
            capture_output=True,
            timeout=timeout + 2
        )
        code = result.stdout.decode().strip()
        return True if code.startswith('2') or code.startswith('3') else False
    except:
        return False

def classify_url(url):
    """对 URL 分类：ipv6, dual, ipv4"""
    if is_ipv6_url(url):
        return 'ipv6'
    elif is_ipv4_url(url) or is_rtp(url):
        return 'ipv4'
    else:
        # https 或其他，可能是双栈
        return 'dual'

def build_url_key(url):
    """生成 URL 唯一键，用于去重"""
    return url.strip()

def process_channels(channels_data):
    """处理频道数据：过滤、聚合线路、测试 IPv6"""
    result = []
    stats = {
        'total_channels': 0,
        'total_lines': 0,
        'by_group': defaultdict(lambda: {'channels': 0, 'lines': 0}),
        'filtered_out': 0
    }
    
    # 按分组处理
    for (group, name), urls in channels_data.items():
        # 只处理有效分组
        if group not in VALID_GROUPS:
            stats['filtered_out'] += len(urls)
            continue
        
        # 过滤非电视台
        if not filter_channel(name, group):
            stats['filtered_out'] += len(urls)
            continue
        
        # 对 URL 分类
        ipv6_urls = []
        dual_urls = []
        ipv4_urls = []
        unique_urls = set()
        
        for url in urls:
            url = url.strip()
            if not url or url in unique_urls:
                continue
            unique_urls.add(url)
            
            # 检查是否包含过滤关键词
            if any(kw in url.lower() for kw in ['bdstatic.com', '支持作者', '轮播']):
                continue
                
            url_type = classify_url(url)
            if url_type == 'ipv6':
                ipv6_urls.append(url)
            elif url_type == 'dual':
                dual_urls.append(url)
            else:
                ipv4_urls.append(url)
        
        # 测试 IPv6 超时
        valid_ipv6 = []
        timeout_ipv6 = []
        
        for url in ipv6_urls:
            # 仅对 IPv6 进行 5 秒超时测试
            # 假设网络可用的 IPv6 URL 应该能快速响应
            # 这里简化处理：直接保留所有 IPv6，但标记出来
            # 实际测试需要网络支持
            if test_url_timeout(url, timeout=5):
                valid_ipv6.append(url)
            else:
                timeout_ipv6.append(url)
        
        # 重新排序：的有效 IPv6 > 超时 IPv6 > 双栈 > IPv4
        all_urls = valid_ipv6 + timeout_ipv6 + dual_urls + ipv4_urls
        
        if all_urls:
            result.append((group, name, all_urls))
            stats['total_channels'] += 1
            stats['total_lines'] += len(all_urls)
            stats['by_group'][group]['channels'] += 1
            stats['by_group'][group]['lines'] += len(all_urls)
    
    return result, stats

def write_m3u(channels, output_path):
    """写入处理后的 m3u 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        
        for group, name, urls in channels:
            for url in urls:
                f.write(f'#EXTINF:-1 group-title="{group}",{name}\n')
                f.write(f'{url}\n')

def main():
    input_file = 'iptv.m3u'
    output_file = 'iptv_new.m3u'
    
    print(f"正在读取 {input_file}...")
    content = read_m3u(input_file)
    
    print("正在解析 m3u...")
    channels_data = parse_m3u(content)
    print(f"解析到 {len(channels_data)} 个频道条目")
    
    print("正在处理频道（过滤、聚合、测试 IPv6）...")
    result, stats = process_channels(channels_data)
    
    # 按分组排序
    group_order = {g: i for i, g in enumerate(VALID_GROUPS)}
    result.sort(key=lambda x: (group_order.get(x[0], 99), x[1]))
    
    print(f"正在写入 {output_file}...")
    write_m3u(result, output_file)
    
    # 输出统计
    print("\n" + "="*50)
    print("处理统计:")
    print(f"  总频道数：{stats['total_channels']}")
    print(f"  总线路数：{stats['total_lines']}")
    print(f"  平均线路/频道：{stats['total_lines']/max(1,stats['total_channels']):.2f}")
    print(f"  过滤掉条目: {stats['filtered_out']}")
    
    print("\n  按分组统计:")
    for g in VALID_GROUPS:
        if stats['by_group'][g]['channels'] > 0:
            avg = stats['by_group'][g]['lines'] / stats['by_group'][g]['channels']
            print(f"    {g}: {stats['by_group'][g]['channels']} 频道, {stats['by_group'][g]['lines']} 线路, 平均 {avg:.1f} 线路/频道")
    
    return result, stats

if __name__ == '__main__':
    result, stats = main()
    print("\n完成!")