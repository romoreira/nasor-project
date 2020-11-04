/* SPDX-License-Identifier: GPL-2.0 */
#include <stddef.h>
#include <linux/bpf.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/ip.h>
#include <linux/icmpv6.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
/* Defines xdp_stats_map from packet04 */
#include "../common/xdp_stats_kern_user.h"
#include "../common/xdp_stats_kern.h"

#define ETH_P_IPV4 0x0800

/* Header cursor to keep track of current parsing position */
struct hdr_cursor {
	void *pos;
};

// Nicer way to call bpf_trace_printk()
#define bpf_custom_printk(fmt, ...)                     \
        ({                                              \
            char ____fmt[] = fmt;                       \
            bpf_trace_printk(____fmt, sizeof(____fmt),  \
                    ##__VA_ARGS__);                     \
        })

/* Packet parsing helpers.
 *
 * Each helper parses a packet header, including doing bounds checking, and
 * returns the type of its contents if successful, and -1 otherwise.
 *
 * For Ethernet and IP headers, the content type is the type of the payload
 * (h_proto for Ethernet, nexthdr for IPv6), for ICMP it is the ICMP type field.
 * All return values are in host byte order.
 */
/*static __always_inline int parse_ethhdr(struct hdr_cursor *nh,
					void *data_end,
					struct ethhdr **ethhdr)

{
	struct ethhdr *eth = nh->pos;
	int hdrsize = sizeof(*eth);

//	__u32 eth_proto;
	__u32 nh_off;

	nh_off = sizeof(struct ethhdr);

	// Byte-count bounds check; check if current pointer + size of header
	// is after data_end.
	
	if (nh->pos + nh_off > data_end)
		return -1;


	nh->pos += hdrsize;
	*ethhdr = eth;

	return eth->h_proto; // network-byte-order
}*/

/* Assignment 2: Implement and use this */
/*static __always_inline int parse_ip6hdr(struct hdr_cursor *nh,
					void *data_end,
					struct ipv6hdr **ip6hdr)
{
	struct ethhdr *eth = nh->pos;
	struct ipv6hdr *ip6h = nh->pos;
	int hdrsize = sizeof(*ip6h);

        __u32 nh_off;
        nh_off = hdrsize;


	if (ip6h + 1 > data_end)
		return -1;

	nh->pos += hdrsize;
        *ip6hdr = ip6h;

        return eth->h_proto; // network-byte-order

}*/

/* Assignment 3: Implement and use this */
/*static __always_inline int parse_icmp6hdr(struct hdr_cursor *nh,
					  void *data_end,
					  struct icmp6hdr **icmp6hdr)
{
}*/

SEC("xdp_packet_parser")
int  xdp_parser_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
//	struct ethhdr *eth;
	struct ipv6hdr *ip6h;//Para IPv6

	/* Default action XDP_PASS, imply everything we couldn't parse, or that
	 * we don't want to deal with, we just pass up the stack and let the
	 * kernel deal with it.
	 */
	__u32 action = XDP_PASS; /* Default action */

        /* These keep track of the next header type and iterator pointer */
	struct hdr_cursor nh;
//	int nh_type;

	/* Start next header cursor position at data start */
	nh.pos = data;

	/* Packet parsing in steps: Get each header one at a time, aborting if
	 * parsing fails. Each helper function does sanity checking (is the
	 * header type in the packet correct?), and bounds checking.
	 */
	//nh_type = parse_ethhdr(&nh, data_end, &eth);

	struct icmp6hdr *icmp6h;

	struct ethhdr *eth = data;
	if ((void*)eth + sizeof(*eth) <= data_end){
		bpf_custom_printk("Tipo de pacote eth %u\n",eth->h_proto);
		if(eth->h_proto == bpf_htons(ETH_P_IPV4)){
			bpf_custom_printk("Pacote nao eh IPv6\n");
                        goto out;
		}
		ip6h = data + sizeof(*eth);
		if ((void*)ip6h + sizeof(*ip6h) <= data_end) {
			bpf_custom_printk("Pacote eh IPv6 Verificando se ele e ICMPv6\n");
			icmp6h = data + sizeof(*eth)  + sizeof(*ip6h);
			if ((void*)icmp6h + sizeof(*icmp6h) <= data_end){
				bpf_custom_printk("Pacote eh ICMPv6, sequence number: %d\n", bpf_htons(icmp6h->icmp6_sequence));
				action = XDP_DROP;
				return xdp_stats_record_action(ctx, action); /* read via xdp_stats */
			}
		}
		else{
			bpf_custom_printk("Pacote nao eh ICMPv6\n");
			goto out;
		}

	}



//	nh_type = parse_ip6hdr(&nh, data_end, &ip6h);
//	bpf_custom_printk("Valor de nh_type = %d e valor de bpf_htons(ETH_P_IPV6) = %d\n",nh_type, bpf_htons(ETH_P_IPV4)); // <-- Adicionar essa linha
//	if (nh_type != bpf_htons(ETH_P_IPV4))
//		goto out;

	/* Assignment additions go below here */

//	action = XDP_DROP;
out:
	return xdp_stats_record_action(ctx, action); /* read via xdp_stats */
}
char _license[] SEC("license") = "GPL";
