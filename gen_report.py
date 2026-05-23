#!/usr/bin/env python3
"""Generate UPDATE_REPORT.md for IPTV repo."""
import re
from collections import Counter
from datetime import datetime

with open('/root/workspace/iptv-jh-repo/iptv.m3u', encoding='utf-8') as f:
    content = f.read()

inf_lines = [l for l in content.split('\n') if l.startswith('#EXTINF:')]
total = len(inf_lines)
cctv = content.count('group-title="央视频道"')
weishi = content.count('group-title="卫视频道"')

channel_names = []
for m in re.finditer(r',(.+)', content):
    name = m.group(1).strip()
    if name and not name.startswith('#'):
        channel_names.append(name)

unique = sorted(set(channel_names))
counter = Counter(channel_names)
now = datetime.now().strftime('%Y年%m月%d日 %H:%M')

report = f"""# IPTV 直播源更新报告

## 基本信息
- **生成时间**: {now}
- **源仓库**: https://github.com/michaelactions/iptv-jh
- **合并来源**: fanmingming/live, iptv-org/iptv

## 统计数据

| 统计项 | 数值 |
|--------|------|
| 频道总数 | {len(unique)} |
| 总线路数 | {total} |
| 央视频道线路 | {cctv} |
| 卫视频道线路 | {weishi} |
| 其他频道线路 | {total - cctv - weishi} |

## 多线路频道 Top 20

| 频道 | 线路数 |
|------|--------|
"""
for name, count in counter.most_common(20):
    report += f"| {name} | {count} |\n"

report += """
## 分组统计
- **央视频道**: 涵盖 CCTV-1 至 CCTV-17、CCTV-4K、CCTV-8K、CGTN 多语种
- **卫视频道**: 全国各省市卫视台
- **地方频道**: 各省市地方台及特色频道

## 更新内容
- 从多个源合并最新直播源
- 频道名标准化，去除分辨率/质量标签
- 每条频道多线路支持，IPv6 > IPv4 排序
"""

with open('/root/workspace/iptv-jh-repo/UPDATE_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ UPDATE_REPORT.md 已生成")
print(f"   频道总数: {len(unique)}")
print(f"   总线路数: {total}")