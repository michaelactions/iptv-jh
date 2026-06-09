# iptv-jh

自动整理的 IPTV 直播源列表，通过**重庆电信家宽**实测可播。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `iptv.m3u` | ✅ **直播源列表（唯一文件）** 内置 EPG 节目单头信息，即订阅即用 |

## 🚀 一键订阅

### 国内加速

```text
https://proxya.pp.ua/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv.m3u
```

或

```text
https://www.proxya.pp.ua/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv.m3u
```

或

```text
https://ghproxy.net/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv.m3u
```

或

```text
https://fastly.jsdelivr.net/gh/michaelactions/iptv-jh@main/iptv.m3u
```

### 直接链接（国外）

```text
https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv.m3u
```

## 📺 使用方法

把上面的链接导入任何支持 M3U 的播放器即可。

| 平台 | 推荐软件 |
|------|---------|
| 安卓 TV | TiviMate |
| iOS | APTV, zFuse |
| 电脑 | PotPlayer, VLC |
| 电视盒子 | DIYP 影音 |

## 📊 当前统计

| 项目 | 数值 |
|------|------|
| 总频道 | 518 |
| 总线路 | 672 |
| 央视频道 | 21 |
| 卫视频道 | 37 |
| 地方/其他 | 460 |
| 多线路频道 | 93 |

## 🔧 技术说明

### 数据来源

从多个来源全网搜索并聚合（best-fan/fanmingming/iptv-org/imDazui 等），通过 **npg（重庆电信家宽）** 的 SSH 隧道下载并逐条验证连通性，仅保留国内可播的源。

### 更新机制

- **更新频率**：每天 06:30（CST）
- **流程**：建 SSH 隧道 → 下载所有源 → 解析去重 → 隧道内验证连通性 → 推送 GitHub
- **失败降级**：隧道不通时自动跳过验证，直接聚合已有源

### EPG 节目单

M3U 文件头部已内置 `x-tvg-url=https://live.fanmingming.cn/e.xml`，支持 EPG 的播放器（TiviMate/APTV 等）会自动加载节目信息。

## ⚠️ 注意事项

1. **部分频道可能需要 IPv6 网络**才能播放（单独保留，不做删除）
2. 重庆电信家宽实测通过率约 20% — 运营商不同效果会有差异
3. 建议每周刷新一次订阅
4. 旧版 `iptv-with-epg.m3u` 已废弃删除，请迁移到 `iptv.m3u`

## 📞 问题反馈

频道无法播放？切换备用线路或检查自己的网络环境。
