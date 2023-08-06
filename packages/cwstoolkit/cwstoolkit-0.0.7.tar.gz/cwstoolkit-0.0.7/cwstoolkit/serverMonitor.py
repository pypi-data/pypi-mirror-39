#!/usr/bin/env python
# encoding: utf-8
# Author: Colin
# Date: 2018
# Desc:
#

import subprocess

class Server():
	"""
	## warn
	告警 - 资源[${resource}]；当前值[${currentValue}] - 阈值[${threshold}]；备注：${remark}
	{"resouce": "cpu", "currentValue": "95%", "threshold": "80%", "remark": "192.168.2.52 4core"}

	## recovery
	恢复 - 资源[${resource}]；当前值[${currentValue}]；备注：${remark}
	{"resouce": "cpu", "currentValue": "2.3%", "remark": "192.168.2.4"}
	"""

	def __init__(self, threshold=80, eth='eth0',processname=None, partition='/'):
		self.threshold = threshold
		self.eth = eth
		self.processname = processname
		self.partition = partition

	def getCpuCount(self):
		cmd = "cat /proc/cpuinfo|grep processor|wc -l"
		record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		count = record.stdout.read().decode('utf-8').split('\n')[0]
		return int(count)

	def getIP(self):
		cmd = "ifconfig %s|grep inet|awk '{print $2}'" % self.eth
		record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		ipaddr = record.stdout.read().decode('utf-8').split('\n')[0]
		return ipaddr


	def checkLoad5(self):
		cmd = "uptime"
		msg = {}
		cpucount = self.getCpuCount()
		hostip = self.getIP()
		load_threshold = cpucount * self.threshold / 100
		origin_record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		load5 = origin_record.stdout.read().decode('utf-8').split(',')[4].strip()
		if float(load5) > load_threshold:
			msg['resource'] = 'Load5'
			msg['currentValue'] = '%.2f' % float(load5)
			msg['threshold'] = load_threshold
			msg['remark'] = '主机%s 5分钟负载超过' % hostip
			msg['detail'] = '主机%s 5分钟负载超过%.2f,当前值%.2f' % (hostip, load_threshold, float(load5))
		return msg

	def checkDisk(self):

		msg = {}
		hostip = self.getIP()
		disk_threshold = self.threshold
		cmd = "df -h %s |grep -v Filesystem|grep -v ':'|egrep -v docker|awk '{print $2,$3,$5,$6}'" % self.partition
		origin_record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		record = origin_record.stdout.read().decode('utf-8')

		msg['resource'] = 'Disk'
		item = record.split('\n')[0]
		total = item.split(' ')[0]
		used = item.split(' ')[1]
		usedpercent = item.split(' ')[2]
		# partition = item.split(' ')[3]
		if int(usedpercent.split('%')[0]) > disk_threshold:
			msg['currentValue'] = '%s' % usedpercent
			msg['threshold'] = '%d%%' % disk_threshold
			msg['remark'] = '主机%s磁盘分区%s' % (hostip,self.partition)
			msg['detail'] = '主机%s磁盘分区%s超过%d%%, 当前值%s' % (hostip, self.partition, disk_threshold, usedpercent)
		return msg


	def checkMemory(self):
		msg = {}
		hostip = self.getIP()
		mem_threshold = self.threshold
		cmd = "free -m|grep Mem|awk '{print $2,$3,$NF}'"
		origin_record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		record = origin_record.stdout.read().decode('utf-8')
		msg['resource'] = 'Memory'
		total = int(record.split(' ')[0])
		used = int(record.split(' ')[1])
		available = int(record.split(' ')[2])

		if used/total*100 > mem_threshold:
			msg['currentValue'] = '%dm' % used
			msg['threshold'] = '%d%%' % mem_threshold
			msg['remark'] = '主机%s总内存%dm' % (hostip,total)
			msg['detail'] = '主机%s内存使用超过%d%%, 当前使用%dm,总%dm' %  (hostip, mem_threshold,  used, total)

		return msg


	def checkCpu(self):
		msg = {}
		hostip = self.getIP()
		cpu_threshold = self.threshold
		cmd = "top -b -n 1|grep Cpu|awk '{print $2,$4,$10}'"
		origin_record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		record = origin_record.stdout.read().decode('utf-8')
		msg['resource'] = 'CPU'
		user = float(record.split(' ')[0])
		sys = float(record.split(' ')[1])
		iowait = float(record.split(' ')[2])

		if user > cpu_threshold or sys > cpu_threshold or iowait > cpu_threshold :
			msg['currentValue'] = 'user:%.2f;sys:%.2f,iowait:%.2f' % (user,sys,iowait)
			msg['threshold'] = '%d%%' % cpu_threshold
			msg['remark'] = '主机%s CPU某项值(用户态,系统太,iowait)' % hostip
			msg['detail'] = '主机%s CPU某项值(用户态,系统太,iowait)使用超过%d%%, 当前值-user:%.2f;sys:%.2f,iowait:%.2f'  %  (hostip, cpu_threshold, user,sys,iowait)

		return msg

	def checkProcess(self):
		msg = {}
		hostip = self.getIP()
		cmd = "ps -ef | grep '%s' | grep  -v grep | wc -l" % self.processname
		origin_record = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		count = eval(origin_record.stdout.read())
		msg['resource'] = 'Process'

		if count != 1:
			msg['currentValue'] = '进程个数%d' % count
			msg['threshold'] = 1
			msg['remark'] = '主机%s 服务%s 存在异常' % (hostip, processname)
			msg['detail'] = '主机%s 服务%s 存在异常，进程个数%d' % (hostip, processname, count)

		return msg

