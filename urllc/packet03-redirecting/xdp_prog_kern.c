/* SPDX-License-Identifier: GPL-2.0 */
#include <linux/bpf.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include <linux/seg6.h>

// The parsing helper functions from the packet01 lesson have moved here
#include "../common/parsing_helpers.h"

/* Defines xdp_stats_map */
#include "../common/xdp_stats_kern_user.h"
#include "../common/xdp_stats_kern.h"

#define ETH_P_IPV4 0x0800


#ifndef memcpy
#define memcpy(dest, src, n) __builtin_memcpy((dest), (src), (n))
#endif

// Nicer way to call bpf_trace_printk()
#define bpf_custom_printk(fmt, ...)                     \
        ({                                              \
            char ____fmt[] = fmt;                       \
            bpf_trace_printk(____fmt, sizeof(____fmt),  \
                    ##__VA_ARGS__);                     \
        })


struct bpf_map_def SEC("maps") tx_port = {
	.type = BPF_MAP_TYPE_DEVMAP,
	.key_size = sizeof(int),
	.value_size = sizeof(int),
	.max_entries = 256,
};

struct bpf_map_def SEC("maps") redirect_params = {
	.type = BPF_MAP_TYPE_HASH,
	.key_size = ETH_ALEN,
	.value_size = ETH_ALEN,
	.max_entries = 1,
};
static __always_inline void swap_src_dst_mac(struct ethhdr *eth)
{
	/* Assignment 1: swap source and destination addresses in the eth.
	 * For simplicity you can use the memcpy macro defined above */
}

static __always_inline void swap_src_dst_ipv6(struct ipv6hdr *ipv6)
{
	/* Assignment 1: swap source and destination addresses in the iphv6dr */
}

static __always_inline void swap_src_dst_ipv4(struct iphdr *iphdr)
{
	/* Assignment 1: swap source and destination addresses in the iphdr */
}

/* Implement packet03/assignment-1 in this section */
SEC("xdp_icmp_echo")
int xdp_icmp_echo_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
	struct hdr_cursor nh;
	struct ethhdr *eth;
	int eth_type;
	int ip_type;
	int icmp_type;
	struct iphdr *iphdr;
	struct ipv6hdr *ipv6hdr;
	__u16 echo_reply;
	struct icmphdr_common *icmphdr;
	__u32 action = XDP_PASS;

	/* These keep track of the next header type and iterator pointer */
	nh.pos = data;

	/* Parse Ethernet and IP/IPv6 headers */
	eth_type = parse_ethhdr(&nh, data_end, &eth);
	if (eth_type == bpf_htons(ETH_P_IP)) {
		ip_type = parse_iphdr(&nh, data_end, &iphdr);
		if (ip_type != IPPROTO_ICMP)
			goto out;
	} else if (eth_type == bpf_htons(ETH_P_IPV6)) {
		ip_type = parse_ip6hdr(&nh, data_end, &ipv6hdr);
		if (ip_type != IPPROTO_ICMPV6)
			goto out;
	} else {
		goto out;
	}

	/*
	 * We are using a special parser here which returns a stucture
	 * containing the "protocol-independent" part of an ICMP or ICMPv6
	 * header.  For purposes of this Assignment we are not interested in
	 * the rest of the structure.
	 */
	icmp_type = parse_icmphdr_common(&nh, data_end, &icmphdr);
	if (eth_type == bpf_htons(ETH_P_IP) && icmp_type == ICMP_ECHO) {
		/* Swap IP source and destination */
		swap_src_dst_ipv4(iphdr);
		echo_reply = ICMP_ECHOREPLY;
	} else if (eth_type == bpf_htons(ETH_P_IPV6)
		   && icmp_type == ICMPV6_ECHO_REQUEST) {
		/* Swap IPv6 source and destination */
		swap_src_dst_ipv6(ipv6hdr);
		echo_reply = ICMPV6_ECHO_REPLY;
	} else {
		goto out;
	}

	/* Swap Ethernet source and destination */
	swap_src_dst_mac(eth);

	/* Assignment 1: patch the packet and update the checksum. You can use
	 * the echo_reply variable defined above to fix the ICMP Type field. */

	action = XDP_TX;

out:
	return xdp_stats_record_action(ctx, action);
}








SEC("xdp_redirect")
int xdp_redirect_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
	struct hdr_cursor nh;
	struct ethhdr *eth;
	int eth_type;
	int action = XDP_PASS;
	unsigned char dst[ETH_ALEN] = {0x2a, 0x38, 0xdb, 0x0a, 0x5d, 0x6c}; /*2a:38:db:0a:5d:6c*/
	unsigned ifindex = 5;

	/* These keep track of the next header type and iterator pointer */
	nh.pos = data;

	/* Parse Ethernet and IP/IPv6 headers */
	eth_type = parse_ethhdr(&nh, data_end, &eth);
	if (eth_type == -1)
		goto out;


	//bpf_map_lookup_elem(&tx_port, &port);

	bpf_custom_printk("Encaminhando origem: %x:%x  para destino: %x\n", eth->h_source[4],eth->h_source[5], dst[5]);

	memcpy(eth->h_dest, dst, ETH_ALEN);

        action = bpf_redirect(ifindex, 0);

out:
	return xdp_stats_record_action(ctx, action);
}

/* Assignment 3: nothing to do here, patch the xdp_prog_user.c program */
SEC("xdp_redirect_map")
int xdp_redirect_map_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
	struct hdr_cursor nh;
	int action = XDP_PASS;


	/* These keep track of the next header type and iterator pointer */
	nh.pos = data;

//      unsigned char *dst;
//	struct ethhdr *eth;
//     	int eth_type;	
//	eth_type = parse_ethhdr(&nh, data_end, &eth);
//	if (eth_type == -1)
//		goto out;

	unsigned char dst[ETH_ALEN] = {0x08, 0x00, 0x27, 0x2d, 0x25, 0xa0}; /*08:00:27:2d:25:a0*/
        unsigned ifindex = 4;


	struct ipv6hdr *ip6h;
        struct ipv6_sr_hdr *srhv6;
	struct ethhdr *eth = data;
	struct in6_addr *ipv6_list;
	if ((void*)eth + sizeof(*eth) <= data_end){
		bpf_custom_printk("Tipo de pacote eth %u\n",eth->h_proto);
		if(eth->h_proto == bpf_htons(ETH_P_IPV4)){
			bpf_custom_printk("Pacote nao eh IPv6\n");
                        goto out;
		}
		ip6h = data + sizeof(*eth);
		srhv6 = data + sizeof(*eth) + sizeof(*ip6h);
		ipv6_list = srhv6->segments + 1;
		if ((void*)ipv6_list + sizeof(*ipv6_list) <= data_end) {
			bpf_custom_printk("Sements_left without HTONS %x\n", srhv6->segments_left);
			bpf_custom_printk("IPv6 da lista de Segmentos para Encaminhamento %x\n", bpf_htons(ipv6_list->s6_addr16[0]));
			
			bpf_custom_printk("Encaminhando MAC destino:  %x\n", dst[5]);
		        memcpy(eth->h_dest, dst, ETH_ALEN);
			action = bpf_redirect(ifindex, 0);

		}
	}
	else{
		bpf_custom_printk("Pacote nao eh ICMPv6\n");
		goto out;
	}


//	/* Do we know where to redirect this packet? */
//	dst = bpf_map_lookup_elem(&redirect_params, eth->h_source);
//	if (!dst)
//		goto out;

//	/* Set a proper destination address */
//	memcpy(eth->h_dest, dst, ETH_ALEN);
//	action = bpf_redirect_map(&tx_port, 0, 0);

out:
	return xdp_stats_record_action(ctx, action);
}

SEC("xdp_pass")
int xdp_pass_func(struct xdp_md *ctx)
{
	int action = XDP_PASS;
	return xdp_stats_record_action(ctx, action);
}

char _license[] SEC("license") = "GPL";
