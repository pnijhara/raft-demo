"""Functions used for discovery of other services/replicas."""
import logging
from typing import Dict, List

from dns import resolver, reversename

logger: logging.Logger = logging.getLogger(__name__)


def get_hostname_by_ip(address: str) -> str:
    """
    Reverse-lookup an IP-Address to get its corresponding hostname

    Parameters
    ----------
    address : str
        address to be looked up

    Returns
    -------
    str
        hostname if successful
    """
    reverse_name = reversename.from_address(address)
    return str(resolver.resolve(str(reverse_name), "PTR")[0])


def get_ip_by_hostname(hostname: str, record_type: str = "A") -> resolver.Answer:
    """
    Resolve DNS record of type `record_type` to ip address.

    Parameters
    ----------
    hostname : str
        fully qualified domain name
    record_type : str, optional
        DNS record type, by default "A"

    Returns
    -------
    resolver.Answer
        Iterable, ipv4 if type "A", ipv6 if type "AAAA"
    """
    return resolver.resolve(hostname, record_type)


def discover_by_dns(name: str) -> List[str]:
    """
    Use docker builtin DNS capability to find other replicas.

    Parameters
    ----------
    name : str
        app name, which all instances share since they are replicas of each
        other.

    Returns
    -------
    List[str]
        list of ip addresses of all replicas.
    """
    return [str(ip) for ip in get_ip_by_hostname(name)]


def get_replica_name_by_hostname(hostname: str) -> str:
    """
    Return the human-readable replica name, e.g. node_1

    Parameters
    ----------
    hostname : str
        auto-generated hostname passed to service by docker

    Returns
    -------
    str
        the replica name
    """
    return get_hostname_by_ip(discover_by_dns(hostname)[0])


def discover_replicas(app_name: str, hostname: str) -> Dict[str, str]:
    """
    Discover all replicas of this service in the same Docker network.

    This works by specifying a max_replica parameter (can be passed via
    envvar) and utilizing the [Docker DNS Services][0].

    [0]: https://docs.docker.com/config/containers/container-networking/#dns-services

    Parameters
    ----------
    app_name : str
        name of the app shared by all instances

    hostname : str
        own hostname to lookup which of the nodes we are.

    Returns
    -------
    Dict[str, str]
        Map domain names of replicas to their IP addresses.
    """
    ip_addresses = discover_by_dns(app_name)
    # remove own address from that
    own_address = str(get_ip_by_hostname(hostname)[0])
    replicas = {}
    for address in ip_addresses:
        if not address == own_address:
            fqdn = get_hostname_by_ip(address)
            replicas[fqdn] = address

    # TODO: (skowalak) ping every node to know if it is online

    logger.debug("own id and address: %s, %s", hostname, own_address)

    return {k: str(v) for k, v in replicas.items() if v}
