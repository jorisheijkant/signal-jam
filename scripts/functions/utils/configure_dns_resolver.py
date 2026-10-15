import socket
import dns.resolver


def configure_dns_resolver(resolver_ip):
    print(f"Configuring DNS resolver with ip {resolver_ip}")
    if not resolver_ip:
        return

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]
    original_getaddrinfo = socket.getaddrinfo

    def _resolve_via_custom_dns(host, port, family=0, type=0, proto=0, flags=0):
        try:
            resolved_ip = resolver.resolve(host)[0].to_text()
        except dns.exception.DNSException:
            return original_getaddrinfo(host, port, family, type, proto, flags)
        return original_getaddrinfo(resolved_ip, port, family, type, proto, flags)

    socket.getaddrinfo = _resolve_via_custom_dns
