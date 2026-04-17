from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def _handle_ConnectionUp(event):
    log.info("Firewall Started")

def _handle_PacketIn(event):
    packet = event.parsed

    if packet.find('ipv4'):
        ip = packet.find('ipv4')

        if str(ip.srcip) == "10.0.0.1":
            log.info("Blocked packet from %s", ip.srcip)
            return

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)