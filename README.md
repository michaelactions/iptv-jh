# iptv-jh

自动整理的 IPTV 播放列表仓库。

## 📁 文件说明

- `iptv.m3u`：纯播放列表（每日更新）
- `iptv-with-epg.m3u`：**集成电子节目单 (EPG) 的完整版** ⭐ 推荐订阅此文件
- `epg.xml`：电子节目单数据源

## 🚀 一键订阅（推荐）

**只需订阅一个链接，自动包含 EPG 电子节目单！**

### 国内加速链接（推荐）

```text
https://ghproxy.net/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-with-epg.m3u
```

或

```text
https://ghproxy.cc/https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-with-epg.m3u
```

或

```text
https://fastly.jsdelivr.net/gh/michaelactions/iptv-jh@main/iptv-with-epg.m3u
```

### 直接链接（国外）

```text
https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv-with-epg.m3u
```

## 📺 使用方法

**直接把上面的链接导入任何支持 M3U 的播放器即可！**

### 支持的播放器

| 平台 | 推荐软件 | 操作 |
|------|---------|------|
| **安卓 TV** | TiviMate | 添加播放列表 → 粘贴链接 → 完成（EPG 自动加载） |
| **iOS** | APTV, zFuse | 添加订阅 → 粘贴链接 → 完成 |
| **电脑** | PotPlayer, VLC | 打开网络串流 → 粘贴链接 → 完成 |
| **电视盒子** | DIYP 影音 | 设置 → 播放源 → 粘贴链接 → 完成 |

### ✅ 特点

- **无需额外配置 EPG**：订阅链接已内置电子节目单
- **自动更新**：每天凌晨 3 点自动刷新频道和节目单
- **即插即用**：复制粘贴链接即可使用

## 📊 频道统计

- **总频道数**: 205
- **总线路数**: 364
- **平均备用源**: 1.8 个/频道
- **央视频道**: 39
- **卫视频道**: 55
- **地方频道**: 111
- **关键频道多线路覆盖**: 54/73
- **最后更新**: 2026-05-05 06:31


## 🔧 技术说明

### EPG 集成原理

本订阅使用 `#EXTM3U x-tvg-url="..."` 标准格式，在 M3U 文件头部声明 EPG 地址：

```m3u
#EXTM3U x-tvg-url="http://epg.51zmt.top:8000/e.xml"
#EXTINF:-1 tvg-name="CCTV1" tvg-id="256", CCTV1
http://example.com/live.m3u8
```

播放器会自动：
1. 读取 M3U 文件中的 `x-tvg-url` 属性
2. 下载对应的 EPG XML 文件
3. 自动匹配频道和节目信息
4. 显示当前和未来的节目单

### 自动更新机制

- **更新频率**: 每天凌晨 3:00（Asia/Shanghai）
- **更新内容**: 
  - 最新 IPTV 直播源
  - 最新 EPG 电子节目单
  - 自动合并生成 `iptv-with-epg.m3u`
- **失败重试**: 主源失败时自动使用备用源

### EPG 源

- **主源**: `http://epg.51zmt.top:8000/e.xml`（国内稳定）
- **备用源**: `http://epg.pw/xmltv/epg.xml`

## 📋 更新日志

- **2026-04-22**: 新增 EPG 自动集成功能，订阅 `iptv-with-epg.m3u` 即可自动获取电子节目单
- **2026-04-17**: 更新直播源，合并多个数据源，优化国内访问速度
- 之前：自动整理维护

## ⚠️ 注意事项

1. **部分频道可能需要 IPv6 网络**才能播放
2. **EPG 自动加载**：确保播放器开启 EPG 功能（默认开启）
3. **如遇卡顿**：可尝试切换其他频道的备用源
4. **定期更新**：建议每周刷新一次订阅（大多数播放器支持自动刷新）
5. **EPG 源偶尔失效**：已配置备用源，自动切换

## 🆚 文件对比

| 文件 | 用途 | 推荐场景 |
|------|------|---------|
| `iptv.m3u` | 纯频道列表 | 需要自定义 EPG 的用户 |
| `iptv-with-epg.m3u` | **频道 + EPG 集成** | **推荐！即插即用** |
| `epg.xml` | EPG 数据源 | 高级用户自定义使用 |

## 📞 问题反馈

- 频道无法播放：检查网络或切换备用源
- EPG 不显示：确认播放器支持 EPG（TiviMate/APTV 均支持）
- 更新失败：查看日志 `/logs/cron.log`

---

**🎉 现在只需订阅 `iptv-with-epg.m3u`，即可享受完整的 IPTV + 电子节目单服务！**
