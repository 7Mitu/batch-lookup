import argparse
import csv
import sys
import dns.resolver

# 设置 DNS 服务器地址
DNS_SERVER = ['8.8.8.8','1.1.1.1','208.67.222.222']

# 域名解析函数
def resolve_domain(domain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = DNS_SERVER
    try:
        answer = resolver.resolve(domain, 'A')
        return answer[0].to_text()
    except Exception as e:
        return str(e)

# 解析命令行参数
parser = argparse.ArgumentParser(description='批量解析域名的DNS A记录')
parser.add_argument('-f', '--file', required=True, help='输入文件（包含域名的文件）')
parser.add_argument('-o', '--output', default='result.csv', help='输出文件（CSV格式）')
args = parser.parse_args()

# 读取域名并进行解析
with open(args.file, 'r') as domain_file:
    domains = domain_file.read().splitlines()

results = []
for i, domain in enumerate(domains, 1):
    ip_address = resolve_domain(domain)
    results.append([domain, ip_address])
    print(f"处理进度: {i}/{len(domains)} ({domain} : {ip_address})")

# 输出到CSV文件
with open(args.output, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Domain', 'IP Address'])
    writer.writerows(results)

print("解析完成，结果已输出至:", args.output)
