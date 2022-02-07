import proxy_checking as proxy

checker = proxy.ProxyChecker()

with open('proxy/proxylist.txt', 'r') as proxylistfile:
    lines = proxylistfile.readlines()
    formatted_lines = []
    for line in lines:
        formatted_lines.append(line.strip('\n'))
    print(formatted_lines)

proxylist = formatted_lines


for proxy in proxylist:
    result = checker.check_proxy(proxy)
    if result['status']:
        print(f'Working proxy {proxy}.')
        print(result['anonymity'], f'{result["time_response"]}ms', result['country_code'], '\n')
        with open('proxy/woking_proxies.txt', 'a') as working_proxies_file:
            working_proxies_file.write(f'{proxy}\n')
    else:
        print(f'Proxy {proxy} was invalid.\n')

        
