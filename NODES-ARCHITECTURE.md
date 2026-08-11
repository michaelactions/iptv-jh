# 节点架构记录 (2026-08-11 更新)

## 电信主节点: casaos
- SSH: wooo.men:2322, 主机名 armbian, 架构 aarch64 (ARM)
- 出口: 125.81.239.167 (与 npg 同一物理机, 不同服务端口)
- 性能: qq 0.1s / CCTV1源 0.035s — 理论比 npg 快
- 隧道: SOCKS5 127.0.0.1:11087

## 联通主节点: JD
- SSH: cu.wooo.men:1022, 主机名 JD, 联通家宽, 老板青龙跑任务
- 出口: 重庆联通段
- 性能: qq 0.1s / CCTV1源 0.04s
- 隧道: SOCKS5 127.0.0.1:11086

## 备用节点
- web: wooo.men:1012 -> 11081 (电信备1)
- npg_old: wooo.men:2999 -> 11080 (电信备2, 旧 npg 隧道)

## 优先级
主节点优先 (priority=1), 备用按 priority 2/3 排序; get_alive_nodes 按
优先级排序返回, 主节点挂了自动用备用。

## 验证脚本自愈映射 (_tunnel_ssh_ports)
- npg -> wooo.men:2322 (casaos)
- mrs -> cu.wooo.men:1022 (JD)
- web -> wooo.men:1012
- npg_old -> wooo.men:2999
