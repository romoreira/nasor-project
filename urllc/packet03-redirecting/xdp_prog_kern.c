/* SPDX-License-Identifier: GPL-2.0 */
#include <linux/bpf.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include <linux/seg6.h>

// The parsing helper functions from the packet01 lesson have moved here
#include "../common/parsing_helpers.h"

#define ETH_P_IPV4 0x0800

/* Defines xdp_stats_map */
#include "../common/xdp_stats_kern_user.h"
#include "../common/xdp_stats_kern.h"

// Nicer way to call bpf_trace_printk()
#define bpf_custom_printk(fmt, ...)                     \
        ({                                              \
            char ____fmt[] = fmt;                       \
            bpf_trace_printk(____fmt, sizeof(____fmt),  \
                    ##__VA_ARGS__);                     \
        })

#ifndef memcpy
#define memcpy(dest, src, n) __builtin_memcpy((dest), (src), (n))
#endif

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


/*
 * The icmp_checksum_diff function takes pointers to old and new structures and
 * the old checksum and returns the new checksum.  It uses the bpf_csum_diff
 * helper to compute the checksum difference. Note that the sizes passed to the
 * bpf_csum_diff helper should be multiples of 4, as it operates on 32-bit
 * words.
 */



/* Assignment 2 */
SEC("xdp_redirect")
int xdp_redirect_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
	struct hdr_cursor nh;
	struct ethhdr *eth;
	int eth_type;
	int action = XDP_PASS;
	unsigned char dst[ETH_ALEN + 1] = {0x08,0x00,0x27,0x2d,0x25,0xa0, '\0'};/*08:00:27:2d:25:a0*/
	unsigned ifindex = 4; 			/* Assignment 2: fill in with the ifindex of the left interface */
	struct ipv6hdr *ip6h;

	int ip_type;
	int icmp_type;
	struct iphdr *iphdr;

	struct icmphdr_common *icmphdr;
	struct ipv6_sr_hdr *srhv6;
	struct in6_addr *ipv6_list;

	nh.pos = data;

	bpf_custom_printk("Teste inicial\n");

	eth_type = parse_ethhdr(&nh, data_end, &eth);
	if (eth_type == bpf_htons(ETH_P_IP)) {
		ip_type = parse_iphdr(&nh, data_end, &iphdr);
		if (ip_type != IPPROTO_ICMP)
			bpf_custom_printk("Pacote diferente de ICMP passing\n");
			goto out;
	} else if (eth_type == bpf_htons(ETH_P_IPV6)) {
		ip_type = parse_ip6hdr(&nh, data_end, &ip6h);
		if(ip_type == 43 || ip_type == 58){
			bpf_custom_printk("Pacote do tipo IPV6 redirecionando...\n");
			goto redirect;
		}
		bpf_custom_printk("IP type %d\n",ip_type);
		if (ip_type != IPPROTO_ICMPV6)
			bpf_custom_printk("Pacote diferente de ICMPv6\n");
			goto out;
	} else {
		goto out;
	}
out:
	return xdp_stats_record_action(ctx, action);

redirect:

	ip6h = data + sizeof(*eth);
	//icmp6h = data + sizeof(*eth) + sizeof(*ip6h);
	icmp_type = parse_icmphdr_common(&nh, data_end, &icmphdr);

	bpf_custom_printk("IPCMPv6 type %d\n",icmp_type);

	if(icmp_type == 135 || icmp_type == 136){
		bpf_custom_printk("ICMP Neighbor solicitation encapsulaed\n");
		goto out;
	}
	
	srhv6 = data + sizeof(*eth) + sizeof(*ip6h);
	ipv6_list = srhv6->segments + 1;
	if ((void*)ipv6_list + sizeof(*ipv6_list) <= data_end) {
		bpf_custom_printk("Sements_left without HTONS %x\n", srhv6->hdrlen);
	}


        bpf_custom_printk("Encaminhando origem: %x:%x  para destino: %x\n", eth->h_source[4],eth->h_source[5], dst[5]);
        memcpy(eth->h_dest,dst,ETH_ALEN);
        action = bpf_redirect(ifindex,0);
        return xdp_stats_record_action(ctx, action);
}

/* Assignment 3: nothing to do here, patch the xdp_prog_user.c program */
SEC("xdp_redirect_map")
int xdp_redirect_map_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
	struct hdr_cursor nh;
	struct ethhdr *eth;
	int eth_type;
	int action = XDP_PASS;
	unsigned char *dst;

	/* These keep track of the next header type and iterator pointer */
	nh.pos = data;

	/* Parse Ethernet and IP/IPv6 headers */
	eth_type = parse_ethhdr(&nh, data_end, &eth);
	if (eth_type == -1)
		goto out;

	/* Do we know where to redirect this packet? */
	dst = bpf_map_lookup_elem(&redirect_params, eth->h_source);
	if (!dst)
		goto out;

	/* Set a proper destination address */
	memcpy(eth->h_dest, dst, ETH_ALEN);
	action = bpf_redirect_map(&tx_port, 0, 0);

out:
	return xdp_stats_record_action(ctx, action);
}


SEC("xdp_pass")
int xdp_pass_func(struct xdp_md *ctx)
{
	int action = XDP_PASS;	
	xdp_stats_record_action(ctx, action);
	return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
