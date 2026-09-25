#!/usr/bin/env python3
"""
SecureNetX AI - Airport Network Topology
Simulates a segmented airport network (6 isolated zones) using
Mininet + Ryu Controller.

Segments: Airport Operations/AODB | Check-in/Admin | Baggage |
          Passenger WiFi | Security/CCTV | DMZ

Note: All hosts currently share a single /16 range (not separate /24
per segment) so basic connectivity (pingall) can be verified without
needing a router between subnets. Real isolation between segments will
be enforced later via actual block rules in the custom Ryu app (SDN
Policy) - not via subnet boundaries.

How to run:
    Terminal 1 (activate the Ryu environment first):
        source ~/ryu-env/bin/activate
        ryu-manager ryu.app.simple_switch_13 --ofp-tcp-listen-port 6633

    Terminal 2:
        sudo python3 airport_topology.py
"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


def build_airport_network():
    net = Mininet(controller=RemoteController, switch=OVSSwitch,
                  link=TCLink, autoSetMacs=True)

    info('*** Adding Controller (Ryu on port 6633)\n')
    net.addController('c0', controller=RemoteController,
                      ip='127.0.0.1', port=6633)

    info('*** Building Core Switch\n')
    core = net.addSwitch('s1')

    info('*** Segment 1: Airport Operations / AODB - critical\n')
    # Note: Real ATC (Air Traffic Control) belongs to a separate air
    # navigation authority with its own isolated network - it is not
    # part of the airport's own operational network.
    ops_switch = net.addSwitch('s2')
    ops1 = net.addHost('h1', ip='10.0.1.1/16')   # AODB Server
    ops2 = net.addHost('h2', ip='10.0.1.2/16')   # Gate Allocation System

    info('*** Segment 2: Check-in / Admin systems\n')
    admin_switch = net.addSwitch('s3')
    admin1 = net.addHost('h3', ip='10.0.2.1/16')  # Check-in System
    admin2 = net.addHost('h4', ip='10.0.2.2/16')  # Admin Workstation

    info('*** Segment 3: Baggage Handling\n')
    baggage_switch = net.addSwitch('s4')
    baggage1 = net.addHost('h5', ip='10.0.3.1/16')  # Baggage System

    info('*** Segment 4: Passenger WiFi - least trusted\n')
    guest_switch = net.addSwitch('s5')
    guest1 = net.addHost('h6', ip='10.0.4.1/16')  # Guest Device 1
    guest2 = net.addHost('h7', ip='10.0.4.2/16')  # Guest Device 2

    info('*** Segment 5: Security / CCTV\n')
    security_switch = net.addSwitch('s6')
    security1 = net.addHost('h8', ip='10.0.5.1/16')  # CCTV Server

    info('*** Segment 6: DMZ - internet-facing services\n')
    dmz_switch = net.addSwitch('s7')
    dmz1 = net.addHost('h9', ip='10.0.6.1/16')   # Booking Web Server
    dmz2 = net.addHost('h10', ip='10.0.6.2/16')  # API Gateway

    info('*** Linking segments to the core switch\n')
    net.addLink(core, ops_switch)
    net.addLink(core, admin_switch)
    net.addLink(core, baggage_switch)
    net.addLink(core, guest_switch)
    net.addLink(core, security_switch)
    net.addLink(core, dmz_switch)  # will be restricted by strict SDN policy later

    info('*** Linking hosts to their segment switches\n')
    net.addLink(ops1, ops_switch)
    net.addLink(ops2, ops_switch)
    net.addLink(admin1, admin_switch)
    net.addLink(admin2, admin_switch)
    net.addLink(baggage1, baggage_switch)
    net.addLink(guest1, guest_switch)
    net.addLink(guest2, guest_switch)
    net.addLink(security1, security_switch)
    net.addLink(dmz1, dmz_switch)
    net.addLink(dmz2, dmz_switch)

    info('\n*** Starting network...\n')
    net.start()

    info('*** Network is up! Try: pingall\n')
    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    build_airport_network()
