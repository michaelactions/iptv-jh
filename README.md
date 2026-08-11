# iptv-jh

自动整理的 IPTV 直播源列表，通过**重庆电信家宽**实测可播。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `iptv-ct.m3u` | ✅ **电信线路版** — 通过重庆电信家宽节点 (npg) 验证 |
| `iptv-cu.m3u` | ✅ **联通线路版** — 通过联通节点 (mrs) 验证 |

> 两版本均内置 EPG 节目单头信息，即订阅即用。

## 🚀 一键订阅

### 电信版 (iptv-ct.m3u)

国内加速:
```
https://proxya.pp.ua/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-ct.m3u
```

直接链接（国外）:
```
https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-ct.m3u
```

### 联通版 (iptv-cu.m3u)

国内加速:
```
https://proxya.pp.ua/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-cu.m3u
```

直接链接（国外）:
```
https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-cu.m3u
```

## 📊 当前统计

<!--STATS_TABLE-->
| 项目 | 电信 (iptv-ct.m3u) | 联通 (iptv-cu.m3u) |
|------|-------------------|-------------------|
| 总频道 | 765 | 767 |
| 总线路 | 1094 | 1115 |
| 央视频道 | 44 | 44 |
| 卫视频道 | 80 | 81 |
| 港澳台频道 | 76 | 76 |
| 轮播频道 | 0 | 0 |
| 电影频道 | 15 | 15 |
| 地方频道 | 550 | 551 |
| 多线路频道 | 259 | 262 |
| IPv4 源 | 1825 | 1847 |
| IPv6 源 | 257 | 257 |
| 成人频道 | 0 | 0 |
<!-- 更新于 2026-08-11 18:19 -->
<!--/STATS_TABLE-->

## 📺 使用方法

把上面的链接导入任何支持 M3U 的播放器即可。

| 平台 | 推荐软件 |
|------|---------|
| 安卓 TV | TiviMate |
| iOS | APTV, zFuse |
| 电脑 | PotPlayer, VLC |
| 电视盒子 | DIYP 影音 |

## 🔧 技术说明

### 数据来源

从多个来源全网搜索并聚合（best-fan/fanmingming/iptv-org/imDazui 等），通过 **npg（重庆电信）+ mrs（联通）** 多节点 SSH 隧道逐条验证连通性：任意节点可播即保留。IPv6 线路单独保留为备用，不参与 IPv4 节点剔除。

过滤策略：只保留真正的电视台直播。体育只保留 CCTV 体育和地方体育电视台；剔除咪咕/PP 体育/精品体育/篮球足球专题、影视/电影/剧场/动漫/综艺轮播、点播、广播电台等非电视台内容。

### 双版本机制

- **iptv-ct.m3u（电信版）**：通过 npg 节点（重庆电信家宽）可播的源
- **iptv-cu.m3u（联通版）**：通过 mrs 节点（联通）可播的源
- 双网都通的源两个版本都包含
- IPv6 源（无法测试）两个版本均包含

### 更新机制

- **更新频率**：每天 06:30（CST）
- **流程**：建 SSH 隧道 → 下载所有源 → 解析去重 → 隧道内验证连通性 → 更新 README → 推送 GitHub
- **失败降级**：隧道不通时自动跳过验证，直接聚合已有源

### EPG 节目单

M3U 文件头部已内置多节目单源：

```text
https://live.fanmingming.cn/e.xml,https://epg.112114.xyz/pp.xml
```

支持 EPG 的播放器（TiviMate/APTV/Kodi 等）会自动加载节目信息。第二个节目单源用于补充地方台覆盖。

## ⚠️ 注意事项

1. **IPv6 线路已保留并作为备用线路输出**，家宽有 IPv6 时播放器可自动尝试
2. IPv4 线路通过电信/联通节点测试，运营商不同效果会有差异
3. 建议每周刷新一次订阅
4. 旧版 `iptv-with-epg.m3u` 和单文件 `iptv.m3u` 已废弃，请迁移到 `iptv-ct.m3u` / `iptv-cu.m3u`

## 📞 问题反馈

频道无法播放？切换备用线路或检查自己的网络环境。
