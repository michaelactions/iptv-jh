# iptv-jh

一个可订阅的 IPTV 列表（CN + HK + TW，不含澳门）。

- 固定订阅直链（Raw）：
  - https://raw.githubusercontent.com/michaelactions/iptv-jh/main/iptv.m3u

## 特性
- 地区范围：大陆 + 香港 + 台湾（不含澳门）
- 排序：CCTV 在前 → 重庆本地频道 → 其他频道
- 去重与择优：每个频道仅保留一个更优源（优先 HTTPS、HLS；过滤 rtmp/udp 等不通用协议）
- 每日自动刷新：每天 06:00（Asia/Shanghai）基于重庆出口的简单测速与可用性检查，失败将自动回退上一版

## 使用方法
- 在你的 IPTV 播放器里找到“订阅/远程列表/网络播放列表”等入口，粘贴上面的订阅直链即可
- 大多数播放器支持 .m3u 远程订阅（如 TiviMate、IPTV Smarters、Kodi、OTT Navigator 等）

## 注意
- 直播源来自公开网络，可能会随时间波动或失效；本仓库会每日自动刷新并尽量挑选更稳的源
- 如果你手上有更稳定/官方的频道直链，欢迎提交 Issue/PR 或联系维护者；我会把它们设为优先候选

## GitHub Pages（可选）
- 如需更“好记”的链接，可在仓库 Settings → Pages 手动开启 Pages（main 分支 / 根目录）
- 开启后即可通过 Pages 域名访问同一文件（例如 https://<你的用户名>.github.io/iptv-jh/iptv.m3u）

## 更新策略
- 每天 06:00 自动抓取 CN/HK/TW 列表 → 去重择优 → 简单测速（重庆出口）→ 更新 iptv.m3u
- 频道优先级：CCTV → 重庆本地 → 其他

## 免责声明
- 本仓库仅聚合公开可得的测试链接，供学习与技术研究使用，请勿用于任何商业/侵权用途。
