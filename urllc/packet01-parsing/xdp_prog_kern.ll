; ModuleID = 'xdp_prog_kern.c'
source_filename = "xdp_prog_kern.c"
target datalayout = "e-m:e-p:64:64-i64:64-n32:64-S128"
target triple = "bpf"

%struct.bpf_map_def = type { i32, i32, i32, i32, i32 }
%struct.xdp_md = type { i32, i32, i32, i32, i32 }
%struct.ethhdr = type { [6 x i8], [6 x i8], i16 }

@xdp_stats_map = global %struct.bpf_map_def { i32 6, i32 4, i32 16, i32 5, i32 0 }, section "maps", align 4, !dbg !0
@xdp_parser_func.____fmt = private unnamed_addr constant [23 x i8] c"Tipo de pacote eth %u\0A\00", align 1
@xdp_parser_func.____fmt.1 = private unnamed_addr constant [20 x i8] c"Pacote nao eh IPv6\0A\00", align 1
@xdp_parser_func.____fmt.2 = private unnamed_addr constant [48 x i8] c"Pacote eh SRH. Verificando o segments Left: %x\0A\00", align 1
@xdp_parser_func.____fmt.3 = private unnamed_addr constant [22 x i8] c"Pacote nao eh ICMPv6\0A\00", align 1
@_license = global [4 x i8] c"GPL\00", section "license", align 1, !dbg !20
@llvm.used = appending global [3 x i8*] [i8* getelementptr inbounds ([4 x i8], [4 x i8]* @_license, i32 0, i32 0), i8* bitcast (i32 (%struct.xdp_md*)* @xdp_parser_func to i8*), i8* bitcast (%struct.bpf_map_def* @xdp_stats_map to i8*)], section "llvm.metadata"

; Function Attrs: nounwind
define i32 @xdp_parser_func(%struct.xdp_md* nocapture readonly) #0 section "xdp_packet_parser" !dbg !57 {
  %2 = alloca i32, align 4
  %3 = alloca [23 x i8], align 1
  %4 = alloca [20 x i8], align 1
  %5 = alloca [48 x i8], align 1
  %6 = alloca [22 x i8], align 1
  call void @llvm.dbg.value(metadata %struct.xdp_md* %0, metadata !69, metadata !DIExpression()), !dbg !170
  %7 = getelementptr inbounds %struct.xdp_md, %struct.xdp_md* %0, i64 0, i32 1, !dbg !171
  %8 = load i32, i32* %7, align 4, !dbg !171, !tbaa !172
  %9 = zext i32 %8 to i64, !dbg !177
  %10 = inttoptr i64 %9 to i8*, !dbg !178
  call void @llvm.dbg.value(metadata i8* %10, metadata !70, metadata !DIExpression()), !dbg !179
  %11 = getelementptr inbounds %struct.xdp_md, %struct.xdp_md* %0, i64 0, i32 0, !dbg !180
  %12 = load i32, i32* %11, align 4, !dbg !180, !tbaa !181
  %13 = zext i32 %12 to i64, !dbg !182
  %14 = inttoptr i64 %13 to i8*, !dbg !183
  call void @llvm.dbg.value(metadata i8* %14, metadata !71, metadata !DIExpression()), !dbg !184
  call void @llvm.dbg.value(metadata i32 2, metadata !109, metadata !DIExpression()), !dbg !185
  call void @llvm.dbg.value(metadata i8* %14, metadata !110, metadata !DIExpression()), !dbg !186
  call void @llvm.dbg.value(metadata %struct.ethhdr* %18, metadata !130, metadata !DIExpression()), !dbg !187
  %15 = getelementptr i8, i8* %14, i64 14, !dbg !188
  %16 = icmp ugt i8* %15, %10, !dbg !189
  br i1 %16, label %41, label %17, !dbg !190

; <label>:17:                                     ; preds = %1
  %18 = inttoptr i64 %13 to %struct.ethhdr*, !dbg !191
  %19 = getelementptr inbounds [23 x i8], [23 x i8]* %3, i64 0, i64 0, !dbg !192
  call void @llvm.lifetime.start.p0i8(i64 23, i8* nonnull %19) #3, !dbg !192
  call void @llvm.dbg.declare(metadata [23 x i8]* %3, metadata !143, metadata !DIExpression()), !dbg !192
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %19, i8* getelementptr inbounds ([23 x i8], [23 x i8]* @xdp_parser_func.____fmt, i64 0, i64 0), i64 23, i32 1, i1 false), !dbg !192
  %20 = getelementptr inbounds %struct.ethhdr, %struct.ethhdr* %18, i64 0, i32 2, !dbg !192
  %21 = load i16, i16* %20, align 1, !dbg !192, !tbaa !193
  %22 = zext i16 %21 to i32, !dbg !192
  %23 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %19, i32 23, i32 %22) #3, !dbg !192
  call void @llvm.lifetime.end.p0i8(i64 23, i8* nonnull %19) #3, !dbg !196
  %24 = load i16, i16* %20, align 1, !dbg !197, !tbaa !193
  %25 = icmp eq i16 %24, 8, !dbg !198
  br i1 %25, label %26, label %29, !dbg !199

; <label>:26:                                     ; preds = %17
  %27 = getelementptr inbounds [20 x i8], [20 x i8]* %4, i64 0, i64 0, !dbg !200
  call void @llvm.lifetime.start.p0i8(i64 20, i8* nonnull %27) #3, !dbg !200
  call void @llvm.dbg.declare(metadata [20 x i8]* %4, metadata !150, metadata !DIExpression()), !dbg !200
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %27, i8* getelementptr inbounds ([20 x i8], [20 x i8]* @xdp_parser_func.____fmt.1, i64 0, i64 0), i64 20, i32 1, i1 false), !dbg !200
  %28 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %27, i32 20) #3, !dbg !200
  call void @llvm.lifetime.end.p0i8(i64 20, i8* nonnull %27) #3, !dbg !201
  br label %41, !dbg !202

; <label>:29:                                     ; preds = %17
  call void @llvm.dbg.value(metadata i8* %14, metadata !114, metadata !DIExpression(DW_OP_plus_uconst, 54, DW_OP_stack_value)), !dbg !203
  call void @llvm.dbg.value(metadata i8* %33, metadata !141, metadata !DIExpression()), !dbg !204
  %30 = getelementptr i8, i8* %14, i64 78, !dbg !205
  %31 = icmp ugt i8* %30, %10, !dbg !206
  br i1 %31, label %38, label %32, !dbg !207

; <label>:32:                                     ; preds = %29
  %33 = getelementptr inbounds i8, i8* %14, i64 62, !dbg !208
  %34 = getelementptr inbounds [48 x i8], [48 x i8]* %5, i64 0, i64 0, !dbg !209
  call void @llvm.lifetime.start.p0i8(i64 48, i8* nonnull %34) #3, !dbg !209
  call void @llvm.dbg.declare(metadata [48 x i8]* %5, metadata !157, metadata !DIExpression()), !dbg !209
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %34, i8* getelementptr inbounds ([48 x i8], [48 x i8]* @xdp_parser_func.____fmt.2, i64 0, i64 0), i64 48, i32 1, i1 false), !dbg !209
  %35 = load i8, i8* %33, align 4, !dbg !209, !tbaa !210
  %36 = zext i8 %35 to i32, !dbg !209
  %37 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %34, i32 48, i32 %36) #3, !dbg !209
  call void @llvm.lifetime.end.p0i8(i64 48, i8* nonnull %34) #3, !dbg !211
  br label %41, !dbg !212

; <label>:38:                                     ; preds = %29
  %39 = getelementptr inbounds [22 x i8], [22 x i8]* %6, i64 0, i64 0, !dbg !213
  call void @llvm.lifetime.start.p0i8(i64 22, i8* nonnull %39) #3, !dbg !213
  call void @llvm.dbg.declare(metadata [22 x i8]* %6, metadata !164, metadata !DIExpression()), !dbg !213
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %39, i8* getelementptr inbounds ([22 x i8], [22 x i8]* @xdp_parser_func.____fmt.3, i64 0, i64 0), i64 22, i32 1, i1 false), !dbg !213
  %40 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %39, i32 22) #3, !dbg !213
  call void @llvm.lifetime.end.p0i8(i64 22, i8* nonnull %39) #3, !dbg !214
  br label %41, !dbg !215

; <label>:41:                                     ; preds = %1, %32, %38, %26
  %42 = bitcast i32* %2 to i8*, !dbg !216
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %42), !dbg !216
  call void @llvm.dbg.value(metadata i32 2, metadata !222, metadata !DIExpression()) #3, !dbg !216
  store i32 2, i32* %2, align 4, !tbaa !233
  %43 = call i8* inttoptr (i64 1 to i8* (i8*, i8*)*)(i8* bitcast (%struct.bpf_map_def* @xdp_stats_map to i8*), i8* nonnull %42) #3, !dbg !234
  call void @llvm.dbg.value(metadata i8* %43, metadata !223, metadata !DIExpression()) #3, !dbg !235
  %44 = icmp eq i8* %43, null, !dbg !236
  br i1 %44, label %58, label %45, !dbg !238

; <label>:45:                                     ; preds = %41
  %46 = bitcast i8* %43 to i64*, !dbg !239
  %47 = load i64, i64* %46, align 8, !dbg !240, !tbaa !241
  %48 = add i64 %47, 1, !dbg !240
  store i64 %48, i64* %46, align 8, !dbg !240, !tbaa !241
  %49 = load i32, i32* %7, align 4, !dbg !244, !tbaa !172
  %50 = load i32, i32* %11, align 4, !dbg !245, !tbaa !181
  %51 = sub i32 %49, %50, !dbg !246
  %52 = zext i32 %51 to i64, !dbg !247
  %53 = getelementptr inbounds i8, i8* %43, i64 8, !dbg !248
  %54 = bitcast i8* %53 to i64*, !dbg !248
  %55 = load i64, i64* %54, align 8, !dbg !249, !tbaa !250
  %56 = add i64 %55, %52, !dbg !249
  store i64 %56, i64* %54, align 8, !dbg !249, !tbaa !250
  %57 = load i32, i32* %2, align 4, !dbg !251, !tbaa !233
  call void @llvm.dbg.value(metadata i32 %57, metadata !222, metadata !DIExpression()) #3, !dbg !216
  br label %58, !dbg !252

; <label>:58:                                     ; preds = %41, %45
  %59 = phi i32 [ %57, %45 ], [ 0, %41 ]
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %42), !dbg !253
  ret i32 %59, !dbg !254
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.start.p0i8(i64, i8* nocapture) #2

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1) #2

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.end.p0i8(i64, i8* nocapture) #2

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.value(metadata, metadata, metadata) #1

attributes #0 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { argmemonly nounwind }
attributes #3 = { nounwind }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!53, !54, !55}
!llvm.ident = !{!56}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "xdp_stats_map", scope: !2, file: !44, line: 16, type: !45, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final)", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, retainedTypes: !13, globals: !19)
!3 = !DIFile(filename: "xdp_prog_kern.c", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!4 = !{!5}
!5 = !DICompositeType(tag: DW_TAG_enumeration_type, name: "xdp_action", file: !6, line: 2845, size: 32, elements: !7)
!6 = !DIFile(filename: "../headers/linux/bpf.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!7 = !{!8, !9, !10, !11, !12}
!8 = !DIEnumerator(name: "XDP_ABORTED", value: 0)
!9 = !DIEnumerator(name: "XDP_DROP", value: 1)
!10 = !DIEnumerator(name: "XDP_PASS", value: 2)
!11 = !DIEnumerator(name: "XDP_TX", value: 3)
!12 = !DIEnumerator(name: "XDP_REDIRECT", value: 4)
!13 = !{!14, !15, !16}
!14 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: null, size: 64)
!15 = !DIBasicType(name: "long int", size: 64, encoding: DW_ATE_signed)
!16 = !DIDerivedType(tag: DW_TAG_typedef, name: "__u16", file: !17, line: 24, baseType: !18)
!17 = !DIFile(filename: "/usr/include/asm-generic/int-ll64.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!18 = !DIBasicType(name: "unsigned short", size: 16, encoding: DW_ATE_unsigned)
!19 = !{!0, !20, !26, !37}
!20 = !DIGlobalVariableExpression(var: !21, expr: !DIExpression())
!21 = distinct !DIGlobalVariable(name: "_license", scope: !2, file: !3, line: 171, type: !22, isLocal: false, isDefinition: true)
!22 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 32, elements: !24)
!23 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!24 = !{!25}
!25 = !DISubrange(count: 4)
!26 = !DIGlobalVariableExpression(var: !27, expr: !DIExpression())
!27 = distinct !DIGlobalVariable(name: "bpf_trace_printk", scope: !2, file: !28, line: 152, type: !29, isLocal: true, isDefinition: true)
!28 = !DIFile(filename: "../libbpf/src//build/usr/include/bpf/bpf_helper_defs.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!29 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !30, size: 64)
!30 = !DISubroutineType(types: !31)
!31 = !{!32, !33, !35, null}
!32 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!33 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !34, size: 64)
!34 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !23)
!35 = !DIDerivedType(tag: DW_TAG_typedef, name: "__u32", file: !17, line: 27, baseType: !36)
!36 = !DIBasicType(name: "unsigned int", size: 32, encoding: DW_ATE_unsigned)
!37 = !DIGlobalVariableExpression(var: !38, expr: !DIExpression())
!38 = distinct !DIGlobalVariable(name: "bpf_map_lookup_elem", scope: !2, file: !28, line: 33, type: !39, isLocal: true, isDefinition: true)
!39 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !40, size: 64)
!40 = !DISubroutineType(types: !41)
!41 = !{!14, !14, !42}
!42 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !43, size: 64)
!43 = !DIDerivedType(tag: DW_TAG_const_type, baseType: null)
!44 = !DIFile(filename: "./../common/xdp_stats_kern.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!45 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "bpf_map_def", file: !46, line: 33, size: 160, elements: !47)
!46 = !DIFile(filename: "../libbpf/src//build/usr/include/bpf/bpf_helpers.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!47 = !{!48, !49, !50, !51, !52}
!48 = !DIDerivedType(tag: DW_TAG_member, name: "type", scope: !45, file: !46, line: 34, baseType: !36, size: 32)
!49 = !DIDerivedType(tag: DW_TAG_member, name: "key_size", scope: !45, file: !46, line: 35, baseType: !36, size: 32, offset: 32)
!50 = !DIDerivedType(tag: DW_TAG_member, name: "value_size", scope: !45, file: !46, line: 36, baseType: !36, size: 32, offset: 64)
!51 = !DIDerivedType(tag: DW_TAG_member, name: "max_entries", scope: !45, file: !46, line: 37, baseType: !36, size: 32, offset: 96)
!52 = !DIDerivedType(tag: DW_TAG_member, name: "map_flags", scope: !45, file: !46, line: 38, baseType: !36, size: 32, offset: 128)
!53 = !{i32 2, !"Dwarf Version", i32 4}
!54 = !{i32 2, !"Debug Info Version", i32 3}
!55 = !{i32 1, !"wchar_size", i32 4}
!56 = !{!"clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final)"}
!57 = distinct !DISubprogram(name: "xdp_parser_func", scope: !3, file: !3, line: 99, type: !58, isLocal: false, isDefinition: true, scopeLine: 100, flags: DIFlagPrototyped, isOptimized: true, unit: !2, variables: !68)
!58 = !DISubroutineType(types: !59)
!59 = !{!32, !60}
!60 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !61, size: 64)
!61 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "xdp_md", file: !6, line: 2856, size: 160, elements: !62)
!62 = !{!63, !64, !65, !66, !67}
!63 = !DIDerivedType(tag: DW_TAG_member, name: "data", scope: !61, file: !6, line: 2857, baseType: !35, size: 32)
!64 = !DIDerivedType(tag: DW_TAG_member, name: "data_end", scope: !61, file: !6, line: 2858, baseType: !35, size: 32, offset: 32)
!65 = !DIDerivedType(tag: DW_TAG_member, name: "data_meta", scope: !61, file: !6, line: 2859, baseType: !35, size: 32, offset: 64)
!66 = !DIDerivedType(tag: DW_TAG_member, name: "ingress_ifindex", scope: !61, file: !6, line: 2861, baseType: !35, size: 32, offset: 96)
!67 = !DIDerivedType(tag: DW_TAG_member, name: "rx_queue_index", scope: !61, file: !6, line: 2862, baseType: !35, size: 32, offset: 128)
!68 = !{!69, !70, !71, !72, !109, !110, !114, !130, !141, !143, !150, !157, !164}
!69 = !DILocalVariable(name: "ctx", arg: 1, scope: !57, file: !3, line: 99, type: !60)
!70 = !DILocalVariable(name: "data_end", scope: !57, file: !3, line: 101, type: !14)
!71 = !DILocalVariable(name: "data", scope: !57, file: !3, line: 102, type: !14)
!72 = !DILocalVariable(name: "ip6h", scope: !57, file: !3, line: 104, type: !73)
!73 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !74, size: 64)
!74 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "ipv6hdr", file: !75, line: 116, size: 320, elements: !76)
!75 = !DIFile(filename: "/usr/include/linux/ipv6.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!76 = !{!77, !80, !81, !85, !88, !89, !90, !108}
!77 = !DIDerivedType(tag: DW_TAG_member, name: "priority", scope: !74, file: !75, line: 118, baseType: !78, size: 4, flags: DIFlagBitField, extraData: i64 0)
!78 = !DIDerivedType(tag: DW_TAG_typedef, name: "__u8", file: !17, line: 21, baseType: !79)
!79 = !DIBasicType(name: "unsigned char", size: 8, encoding: DW_ATE_unsigned_char)
!80 = !DIDerivedType(tag: DW_TAG_member, name: "version", scope: !74, file: !75, line: 119, baseType: !78, size: 4, offset: 4, flags: DIFlagBitField, extraData: i64 0)
!81 = !DIDerivedType(tag: DW_TAG_member, name: "flow_lbl", scope: !74, file: !75, line: 126, baseType: !82, size: 24, offset: 8)
!82 = !DICompositeType(tag: DW_TAG_array_type, baseType: !78, size: 24, elements: !83)
!83 = !{!84}
!84 = !DISubrange(count: 3)
!85 = !DIDerivedType(tag: DW_TAG_member, name: "payload_len", scope: !74, file: !75, line: 128, baseType: !86, size: 16, offset: 32)
!86 = !DIDerivedType(tag: DW_TAG_typedef, name: "__be16", file: !87, line: 25, baseType: !16)
!87 = !DIFile(filename: "/usr/include/linux/types.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!88 = !DIDerivedType(tag: DW_TAG_member, name: "nexthdr", scope: !74, file: !75, line: 129, baseType: !78, size: 8, offset: 48)
!89 = !DIDerivedType(tag: DW_TAG_member, name: "hop_limit", scope: !74, file: !75, line: 130, baseType: !78, size: 8, offset: 56)
!90 = !DIDerivedType(tag: DW_TAG_member, name: "saddr", scope: !74, file: !75, line: 132, baseType: !91, size: 128, offset: 64)
!91 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "in6_addr", file: !92, line: 33, size: 128, elements: !93)
!92 = !DIFile(filename: "/usr/include/linux/in6.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!93 = !{!94}
!94 = !DIDerivedType(tag: DW_TAG_member, name: "in6_u", scope: !91, file: !92, line: 40, baseType: !95, size: 128)
!95 = distinct !DICompositeType(tag: DW_TAG_union_type, scope: !91, file: !92, line: 34, size: 128, elements: !96)
!96 = !{!97, !101, !105}
!97 = !DIDerivedType(tag: DW_TAG_member, name: "u6_addr8", scope: !95, file: !92, line: 35, baseType: !98, size: 128)
!98 = !DICompositeType(tag: DW_TAG_array_type, baseType: !78, size: 128, elements: !99)
!99 = !{!100}
!100 = !DISubrange(count: 16)
!101 = !DIDerivedType(tag: DW_TAG_member, name: "u6_addr16", scope: !95, file: !92, line: 37, baseType: !102, size: 128)
!102 = !DICompositeType(tag: DW_TAG_array_type, baseType: !86, size: 128, elements: !103)
!103 = !{!104}
!104 = !DISubrange(count: 8)
!105 = !DIDerivedType(tag: DW_TAG_member, name: "u6_addr32", scope: !95, file: !92, line: 38, baseType: !106, size: 128)
!106 = !DICompositeType(tag: DW_TAG_array_type, baseType: !107, size: 128, elements: !24)
!107 = !DIDerivedType(tag: DW_TAG_typedef, name: "__be32", file: !87, line: 27, baseType: !35)
!108 = !DIDerivedType(tag: DW_TAG_member, name: "daddr", scope: !74, file: !75, line: 133, baseType: !91, size: 128, offset: 192)
!109 = !DILocalVariable(name: "action", scope: !57, file: !3, line: 110, type: !35)
!110 = !DILocalVariable(name: "nh", scope: !57, file: !3, line: 113, type: !111)
!111 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "hdr_cursor", file: !3, line: 21, size: 64, elements: !112)
!112 = !{!113}
!113 = !DIDerivedType(tag: DW_TAG_member, name: "pos", scope: !111, file: !3, line: 22, baseType: !14, size: 64)
!114 = !DILocalVariable(name: "srhv6", scope: !57, file: !3, line: 126, type: !115)
!115 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !116, size: 64)
!116 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "ipv6_sr_hdr", file: !117, line: 24, size: 64, elements: !118)
!117 = !DIFile(filename: "/usr/include/linux/seg6.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!118 = !{!119, !120, !121, !122, !123, !124, !125, !126}
!119 = !DIDerivedType(tag: DW_TAG_member, name: "nexthdr", scope: !116, file: !117, line: 25, baseType: !78, size: 8)
!120 = !DIDerivedType(tag: DW_TAG_member, name: "hdrlen", scope: !116, file: !117, line: 26, baseType: !78, size: 8, offset: 8)
!121 = !DIDerivedType(tag: DW_TAG_member, name: "type", scope: !116, file: !117, line: 27, baseType: !78, size: 8, offset: 16)
!122 = !DIDerivedType(tag: DW_TAG_member, name: "segments_left", scope: !116, file: !117, line: 28, baseType: !78, size: 8, offset: 24)
!123 = !DIDerivedType(tag: DW_TAG_member, name: "first_segment", scope: !116, file: !117, line: 29, baseType: !78, size: 8, offset: 32)
!124 = !DIDerivedType(tag: DW_TAG_member, name: "flags", scope: !116, file: !117, line: 30, baseType: !78, size: 8, offset: 40)
!125 = !DIDerivedType(tag: DW_TAG_member, name: "tag", scope: !116, file: !117, line: 31, baseType: !16, size: 16, offset: 48)
!126 = !DIDerivedType(tag: DW_TAG_member, name: "segments", scope: !116, file: !117, line: 33, baseType: !127, offset: 64)
!127 = !DICompositeType(tag: DW_TAG_array_type, baseType: !91, elements: !128)
!128 = !{!129}
!129 = !DISubrange(count: 0)
!130 = !DILocalVariable(name: "eth", scope: !57, file: !3, line: 128, type: !131)
!131 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !132, size: 64)
!132 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "ethhdr", file: !133, line: 159, size: 112, elements: !134)
!133 = !DIFile(filename: "/usr/include/linux/if_ether.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!134 = !{!135, !139, !140}
!135 = !DIDerivedType(tag: DW_TAG_member, name: "h_dest", scope: !132, file: !133, line: 160, baseType: !136, size: 48)
!136 = !DICompositeType(tag: DW_TAG_array_type, baseType: !79, size: 48, elements: !137)
!137 = !{!138}
!138 = !DISubrange(count: 6)
!139 = !DIDerivedType(tag: DW_TAG_member, name: "h_source", scope: !132, file: !133, line: 161, baseType: !136, size: 48, offset: 48)
!140 = !DIDerivedType(tag: DW_TAG_member, name: "h_proto", scope: !132, file: !133, line: 162, baseType: !86, size: 16, offset: 96)
!141 = !DILocalVariable(name: "ipv6_list", scope: !57, file: !3, line: 129, type: !142)
!142 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !91, size: 64)
!143 = !DILocalVariable(name: "____fmt", scope: !144, file: !3, line: 131, type: !147)
!144 = distinct !DILexicalBlock(scope: !145, file: !3, line: 131, column: 3)
!145 = distinct !DILexicalBlock(scope: !146, file: !3, line: 130, column: 44)
!146 = distinct !DILexicalBlock(scope: !57, file: !3, line: 130, column: 6)
!147 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 184, elements: !148)
!148 = !{!149}
!149 = !DISubrange(count: 23)
!150 = !DILocalVariable(name: "____fmt", scope: !151, file: !3, line: 133, type: !154)
!151 = distinct !DILexicalBlock(scope: !152, file: !3, line: 133, column: 4)
!152 = distinct !DILexicalBlock(scope: !153, file: !3, line: 132, column: 44)
!153 = distinct !DILexicalBlock(scope: !145, file: !3, line: 132, column: 6)
!154 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 160, elements: !155)
!155 = !{!156}
!156 = !DISubrange(count: 20)
!157 = !DILocalVariable(name: "____fmt", scope: !158, file: !3, line: 143, type: !161)
!158 = distinct !DILexicalBlock(scope: !159, file: !3, line: 143, column: 4)
!159 = distinct !DILexicalBlock(scope: !160, file: !3, line: 142, column: 58)
!160 = distinct !DILexicalBlock(scope: !145, file: !3, line: 142, column: 7)
!161 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 384, elements: !162)
!162 = !{!163}
!163 = !DISubrange(count: 48)
!164 = !DILocalVariable(name: "____fmt", scope: !165, file: !3, line: 152, type: !167)
!165 = distinct !DILexicalBlock(scope: !166, file: !3, line: 152, column: 4)
!166 = distinct !DILexicalBlock(scope: !160, file: !3, line: 151, column: 7)
!167 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 176, elements: !168)
!168 = !{!169}
!169 = !DISubrange(count: 22)
!170 = !DILocation(line: 99, column: 37, scope: !57)
!171 = !DILocation(line: 101, column: 38, scope: !57)
!172 = !{!173, !174, i64 4}
!173 = !{!"xdp_md", !174, i64 0, !174, i64 4, !174, i64 8, !174, i64 12, !174, i64 16}
!174 = !{!"int", !175, i64 0}
!175 = !{!"omnipotent char", !176, i64 0}
!176 = !{!"Simple C/C++ TBAA"}
!177 = !DILocation(line: 101, column: 27, scope: !57)
!178 = !DILocation(line: 101, column: 19, scope: !57)
!179 = !DILocation(line: 101, column: 8, scope: !57)
!180 = !DILocation(line: 102, column: 34, scope: !57)
!181 = !{!173, !174, i64 0}
!182 = !DILocation(line: 102, column: 23, scope: !57)
!183 = !DILocation(line: 102, column: 15, scope: !57)
!184 = !DILocation(line: 102, column: 8, scope: !57)
!185 = !DILocation(line: 110, column: 8, scope: !57)
!186 = !DILocation(line: 113, column: 20, scope: !57)
!187 = !DILocation(line: 128, column: 17, scope: !57)
!188 = !DILocation(line: 130, column: 17, scope: !146)
!189 = !DILocation(line: 130, column: 32, scope: !146)
!190 = !DILocation(line: 130, column: 6, scope: !57)
!191 = !DILocation(line: 128, column: 23, scope: !57)
!192 = !DILocation(line: 131, column: 3, scope: !144)
!193 = !{!194, !195, i64 12}
!194 = !{!"ethhdr", !175, i64 0, !175, i64 6, !195, i64 12}
!195 = !{!"short", !175, i64 0}
!196 = !DILocation(line: 131, column: 3, scope: !145)
!197 = !DILocation(line: 132, column: 11, scope: !153)
!198 = !DILocation(line: 132, column: 19, scope: !153)
!199 = !DILocation(line: 132, column: 6, scope: !145)
!200 = !DILocation(line: 133, column: 4, scope: !151)
!201 = !DILocation(line: 133, column: 4, scope: !152)
!202 = !DILocation(line: 134, column: 25, scope: !152)
!203 = !DILocation(line: 126, column: 22, scope: !57)
!204 = !DILocation(line: 129, column: 19, scope: !57)
!205 = !DILocation(line: 142, column: 24, scope: !160)
!206 = !DILocation(line: 142, column: 45, scope: !160)
!207 = !DILocation(line: 142, column: 7, scope: !145)
!208 = !DILocation(line: 141, column: 22, scope: !145)
!209 = !DILocation(line: 143, column: 4, scope: !158)
!210 = !{!175, !175, i64 0}
!211 = !DILocation(line: 143, column: 4, scope: !159)
!212 = !DILocation(line: 156, column: 2, scope: !145)
!213 = !DILocation(line: 152, column: 4, scope: !165)
!214 = !DILocation(line: 152, column: 4, scope: !166)
!215 = !DILocation(line: 153, column: 4, scope: !166)
!216 = !DILocation(line: 24, column: 57, scope: !217, inlinedAt: !232)
!217 = distinct !DISubprogram(name: "xdp_stats_record_action", scope: !44, file: !44, line: 24, type: !218, isLocal: true, isDefinition: true, scopeLine: 25, flags: DIFlagPrototyped, isOptimized: true, unit: !2, variables: !220)
!218 = !DISubroutineType(types: !219)
!219 = !{!35, !60, !35}
!220 = !{!221, !222, !223}
!221 = !DILocalVariable(name: "ctx", arg: 1, scope: !217, file: !44, line: 24, type: !60)
!222 = !DILocalVariable(name: "action", arg: 2, scope: !217, file: !44, line: 24, type: !35)
!223 = !DILocalVariable(name: "rec", scope: !217, file: !44, line: 30, type: !224)
!224 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !225, size: 64)
!225 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "datarec", file: !226, line: 10, size: 128, elements: !227)
!226 = !DIFile(filename: "./../common/xdp_stats_kern_user.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!227 = !{!228, !231}
!228 = !DIDerivedType(tag: DW_TAG_member, name: "rx_packets", scope: !225, file: !226, line: 11, baseType: !229, size: 64)
!229 = !DIDerivedType(tag: DW_TAG_typedef, name: "__u64", file: !17, line: 31, baseType: !230)
!230 = !DIBasicType(name: "long long unsigned int", size: 64, encoding: DW_ATE_unsigned)
!231 = !DIDerivedType(tag: DW_TAG_member, name: "rx_bytes", scope: !225, file: !226, line: 12, baseType: !229, size: 64, offset: 64)
!232 = distinct !DILocation(line: 169, column: 9, scope: !57)
!233 = !{!174, !174, i64 0}
!234 = !DILocation(line: 30, column: 24, scope: !217, inlinedAt: !232)
!235 = !DILocation(line: 30, column: 18, scope: !217, inlinedAt: !232)
!236 = !DILocation(line: 31, column: 7, scope: !237, inlinedAt: !232)
!237 = distinct !DILexicalBlock(scope: !217, file: !44, line: 31, column: 6)
!238 = !DILocation(line: 31, column: 6, scope: !217, inlinedAt: !232)
!239 = !DILocation(line: 38, column: 7, scope: !217, inlinedAt: !232)
!240 = !DILocation(line: 38, column: 17, scope: !217, inlinedAt: !232)
!241 = !{!242, !243, i64 0}
!242 = !{!"datarec", !243, i64 0, !243, i64 8}
!243 = !{!"long long", !175, i64 0}
!244 = !DILocation(line: 39, column: 25, scope: !217, inlinedAt: !232)
!245 = !DILocation(line: 39, column: 41, scope: !217, inlinedAt: !232)
!246 = !DILocation(line: 39, column: 34, scope: !217, inlinedAt: !232)
!247 = !DILocation(line: 39, column: 19, scope: !217, inlinedAt: !232)
!248 = !DILocation(line: 39, column: 7, scope: !217, inlinedAt: !232)
!249 = !DILocation(line: 39, column: 16, scope: !217, inlinedAt: !232)
!250 = !{!242, !243, i64 8}
!251 = !DILocation(line: 41, column: 9, scope: !217, inlinedAt: !232)
!252 = !DILocation(line: 41, column: 2, scope: !217, inlinedAt: !232)
!253 = !DILocation(line: 42, column: 1, scope: !217, inlinedAt: !232)
!254 = !DILocation(line: 169, column: 2, scope: !57)
