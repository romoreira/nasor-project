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
@xdp_parser_func.____fmt.2 = private unnamed_addr constant [29 x i8] c"Pacote eh IPv6 sera Dropado\0A\00", align 1
@xdp_parser_func.____fmt.3 = private unnamed_addr constant [22 x i8] c"Pacote nao eh ICMPv6\0A\00", align 1
@_license = global [4 x i8] c"GPL\00", section "license", align 1, !dbg !20
@llvm.used = appending global [3 x i8*] [i8* getelementptr inbounds ([4 x i8], [4 x i8]* @_license, i32 0, i32 0), i8* bitcast (i32 (%struct.xdp_md*)* @xdp_parser_func to i8*), i8* bitcast (%struct.bpf_map_def* @xdp_stats_map to i8*)], section "llvm.metadata"

; Function Attrs: nounwind
define i32 @xdp_parser_func(%struct.xdp_md* nocapture readonly) #0 section "xdp_packet_parser" !dbg !57 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca [23 x i8], align 1
  %5 = alloca [20 x i8], align 1
  %6 = alloca [29 x i8], align 1
  %7 = alloca [22 x i8], align 1
  call void @llvm.dbg.value(metadata %struct.xdp_md* %0, metadata !69, metadata !DIExpression()), !dbg !152
  %8 = getelementptr inbounds %struct.xdp_md, %struct.xdp_md* %0, i64 0, i32 1, !dbg !153
  %9 = load i32, i32* %8, align 4, !dbg !153, !tbaa !154
  %10 = zext i32 %9 to i64, !dbg !159
  %11 = inttoptr i64 %10 to i8*, !dbg !160
  call void @llvm.dbg.value(metadata i8* %11, metadata !70, metadata !DIExpression()), !dbg !161
  %12 = getelementptr inbounds %struct.xdp_md, %struct.xdp_md* %0, i64 0, i32 0, !dbg !162
  %13 = load i32, i32* %12, align 4, !dbg !162, !tbaa !163
  %14 = zext i32 %13 to i64, !dbg !164
  %15 = inttoptr i64 %14 to i8*, !dbg !165
  call void @llvm.dbg.value(metadata i8* %15, metadata !71, metadata !DIExpression()), !dbg !166
  call void @llvm.dbg.value(metadata i32 2, metadata !109, metadata !DIExpression()), !dbg !167
  call void @llvm.dbg.value(metadata i8* %15, metadata !110, metadata !DIExpression()), !dbg !168
  call void @llvm.dbg.value(metadata %struct.ethhdr* %19, metadata !114, metadata !DIExpression()), !dbg !169
  %16 = getelementptr i8, i8* %15, i64 14, !dbg !170
  %17 = icmp ugt i8* %16, %11, !dbg !171
  br i1 %17, label %57, label %18, !dbg !172

; <label>:18:                                     ; preds = %1
  %19 = inttoptr i64 %14 to %struct.ethhdr*, !dbg !173
  %20 = getelementptr inbounds [23 x i8], [23 x i8]* %4, i64 0, i64 0, !dbg !174
  call void @llvm.lifetime.start.p0i8(i64 23, i8* nonnull %20) #3, !dbg !174
  call void @llvm.dbg.declare(metadata [23 x i8]* %4, metadata !125, metadata !DIExpression()), !dbg !174
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %20, i8* getelementptr inbounds ([23 x i8], [23 x i8]* @xdp_parser_func.____fmt, i64 0, i64 0), i64 23, i32 1, i1 false), !dbg !174
  %21 = getelementptr inbounds %struct.ethhdr, %struct.ethhdr* %19, i64 0, i32 2, !dbg !174
  %22 = load i16, i16* %21, align 1, !dbg !174, !tbaa !175
  %23 = zext i16 %22 to i32, !dbg !174
  %24 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %20, i32 23, i32 %23) #3, !dbg !174
  call void @llvm.lifetime.end.p0i8(i64 23, i8* nonnull %20) #3, !dbg !178
  %25 = load i16, i16* %21, align 1, !dbg !179, !tbaa !175
  %26 = icmp eq i16 %25, 8, !dbg !180
  br i1 %26, label %27, label %30, !dbg !181

; <label>:27:                                     ; preds = %18
  %28 = getelementptr inbounds [20 x i8], [20 x i8]* %5, i64 0, i64 0, !dbg !182
  call void @llvm.lifetime.start.p0i8(i64 20, i8* nonnull %28) #3, !dbg !182
  call void @llvm.dbg.declare(metadata [20 x i8]* %5, metadata !132, metadata !DIExpression()), !dbg !182
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %28, i8* getelementptr inbounds ([20 x i8], [20 x i8]* @xdp_parser_func.____fmt.1, i64 0, i64 0), i64 20, i32 1, i1 false), !dbg !182
  %29 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %28, i32 20) #3, !dbg !182
  call void @llvm.lifetime.end.p0i8(i64 20, i8* nonnull %28) #3, !dbg !183
  br label %57, !dbg !184

; <label>:30:                                     ; preds = %18
  call void @llvm.dbg.value(metadata i8* %16, metadata !72, metadata !DIExpression()), !dbg !185
  %31 = getelementptr i8, i8* %15, i64 54, !dbg !186
  %32 = icmp ugt i8* %31, %11, !dbg !187
  br i1 %32, label %54, label %33, !dbg !188

; <label>:33:                                     ; preds = %30
  %34 = getelementptr inbounds [29 x i8], [29 x i8]* %6, i64 0, i64 0, !dbg !189
  call void @llvm.lifetime.start.p0i8(i64 29, i8* nonnull %34) #3, !dbg !189
  call void @llvm.dbg.declare(metadata [29 x i8]* %6, metadata !139, metadata !DIExpression()), !dbg !189
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %34, i8* getelementptr inbounds ([29 x i8], [29 x i8]* @xdp_parser_func.____fmt.2, i64 0, i64 0), i64 29, i32 1, i1 false), !dbg !189
  %35 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %34, i32 29) #3, !dbg !189
  call void @llvm.lifetime.end.p0i8(i64 29, i8* nonnull %34) #3, !dbg !190
  call void @llvm.dbg.value(metadata i32 1, metadata !109, metadata !DIExpression()), !dbg !167
  %36 = bitcast i32* %3 to i8*, !dbg !191
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %36), !dbg !191
  call void @llvm.dbg.value(metadata %struct.xdp_md* %0, metadata !196, metadata !DIExpression()) #3, !dbg !191
  call void @llvm.dbg.value(metadata i32 1, metadata !197, metadata !DIExpression()) #3, !dbg !208
  store i32 1, i32* %3, align 4, !tbaa !209
  %37 = call i8* inttoptr (i64 1 to i8* (i8*, i8*)*)(i8* bitcast (%struct.bpf_map_def* @xdp_stats_map to i8*), i8* nonnull %36) #3, !dbg !210
  call void @llvm.dbg.value(metadata i8* %37, metadata !198, metadata !DIExpression()) #3, !dbg !211
  %38 = icmp eq i8* %37, null, !dbg !212
  br i1 %38, label %52, label %39, !dbg !214

; <label>:39:                                     ; preds = %33
  %40 = bitcast i8* %37 to i64*, !dbg !215
  %41 = load i64, i64* %40, align 8, !dbg !216, !tbaa !217
  %42 = add i64 %41, 1, !dbg !216
  store i64 %42, i64* %40, align 8, !dbg !216, !tbaa !217
  %43 = load i32, i32* %8, align 4, !dbg !220, !tbaa !154
  %44 = load i32, i32* %12, align 4, !dbg !221, !tbaa !163
  %45 = sub i32 %43, %44, !dbg !222
  %46 = zext i32 %45 to i64, !dbg !223
  %47 = getelementptr inbounds i8, i8* %37, i64 8, !dbg !224
  %48 = bitcast i8* %47 to i64*, !dbg !224
  %49 = load i64, i64* %48, align 8, !dbg !225, !tbaa !226
  %50 = add i64 %49, %46, !dbg !225
  store i64 %50, i64* %48, align 8, !dbg !225, !tbaa !226
  %51 = load i32, i32* %3, align 4, !dbg !227, !tbaa !209
  call void @llvm.dbg.value(metadata i32 %51, metadata !197, metadata !DIExpression()) #3, !dbg !208
  br label %52, !dbg !228

; <label>:52:                                     ; preds = %33, %39
  %53 = phi i32 [ %51, %39 ], [ 0, %33 ]
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %36), !dbg !229
  br label %76, !dbg !230

; <label>:54:                                     ; preds = %30
  %55 = getelementptr inbounds [22 x i8], [22 x i8]* %7, i64 0, i64 0, !dbg !231
  call void @llvm.lifetime.start.p0i8(i64 22, i8* nonnull %55) #3, !dbg !231
  call void @llvm.dbg.declare(metadata [22 x i8]* %7, metadata !146, metadata !DIExpression()), !dbg !231
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* nonnull %55, i8* getelementptr inbounds ([22 x i8], [22 x i8]* @xdp_parser_func.____fmt.3, i64 0, i64 0), i64 22, i32 1, i1 false), !dbg !231
  %56 = call i32 (i8*, i32, ...) inttoptr (i64 6 to i32 (i8*, i32, ...)*)(i8* nonnull %55, i32 22) #3, !dbg !231
  call void @llvm.lifetime.end.p0i8(i64 22, i8* nonnull %55) #3, !dbg !232
  br label %57, !dbg !233

; <label>:57:                                     ; preds = %1, %54, %27
  %58 = bitcast i32* %2 to i8*, !dbg !234
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %58), !dbg !234
  call void @llvm.dbg.value(metadata %struct.xdp_md* %0, metadata !196, metadata !DIExpression()) #3, !dbg !234
  call void @llvm.dbg.value(metadata i32 2, metadata !197, metadata !DIExpression()) #3, !dbg !236
  store i32 2, i32* %2, align 4, !tbaa !209
  %59 = call i8* inttoptr (i64 1 to i8* (i8*, i8*)*)(i8* bitcast (%struct.bpf_map_def* @xdp_stats_map to i8*), i8* nonnull %58) #3, !dbg !237
  call void @llvm.dbg.value(metadata i8* %59, metadata !198, metadata !DIExpression()) #3, !dbg !238
  %60 = icmp eq i8* %59, null, !dbg !239
  br i1 %60, label %74, label %61, !dbg !240

; <label>:61:                                     ; preds = %57
  %62 = bitcast i8* %59 to i64*, !dbg !241
  %63 = load i64, i64* %62, align 8, !dbg !242, !tbaa !217
  %64 = add i64 %63, 1, !dbg !242
  store i64 %64, i64* %62, align 8, !dbg !242, !tbaa !217
  %65 = load i32, i32* %8, align 4, !dbg !243, !tbaa !154
  %66 = load i32, i32* %12, align 4, !dbg !244, !tbaa !163
  %67 = sub i32 %65, %66, !dbg !245
  %68 = zext i32 %67 to i64, !dbg !246
  %69 = getelementptr inbounds i8, i8* %59, i64 8, !dbg !247
  %70 = bitcast i8* %69 to i64*, !dbg !247
  %71 = load i64, i64* %70, align 8, !dbg !248, !tbaa !226
  %72 = add i64 %71, %68, !dbg !248
  store i64 %72, i64* %70, align 8, !dbg !248, !tbaa !226
  %73 = load i32, i32* %2, align 4, !dbg !249, !tbaa !209
  call void @llvm.dbg.value(metadata i32 %73, metadata !197, metadata !DIExpression()) #3, !dbg !236
  br label %74, !dbg !250

; <label>:74:                                     ; preds = %57, %61
  %75 = phi i32 [ %73, %61 ], [ 0, %57 ]
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %58), !dbg !251
  br label %76, !dbg !252

; <label>:76:                                     ; preds = %74, %52
  %77 = phi i32 [ %75, %74 ], [ %53, %52 ]
  ret i32 %77, !dbg !253
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
!21 = distinct !DIGlobalVariable(name: "_license", scope: !2, file: !3, line: 158, type: !22, isLocal: false, isDefinition: true)
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
!57 = distinct !DISubprogram(name: "xdp_parser_func", scope: !3, file: !3, line: 97, type: !58, isLocal: false, isDefinition: true, scopeLine: 98, flags: DIFlagPrototyped, isOptimized: true, unit: !2, variables: !68)
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
!68 = !{!69, !70, !71, !72, !109, !110, !114, !125, !132, !139, !146}
!69 = !DILocalVariable(name: "ctx", arg: 1, scope: !57, file: !3, line: 97, type: !60)
!70 = !DILocalVariable(name: "data_end", scope: !57, file: !3, line: 99, type: !14)
!71 = !DILocalVariable(name: "data", scope: !57, file: !3, line: 100, type: !14)
!72 = !DILocalVariable(name: "ip6h", scope: !57, file: !3, line: 102, type: !73)
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
!109 = !DILocalVariable(name: "action", scope: !57, file: !3, line: 108, type: !35)
!110 = !DILocalVariable(name: "nh", scope: !57, file: !3, line: 111, type: !111)
!111 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "hdr_cursor", file: !3, line: 19, size: 64, elements: !112)
!112 = !{!113}
!113 = !DIDerivedType(tag: DW_TAG_member, name: "pos", scope: !111, file: !3, line: 20, baseType: !14, size: 64)
!114 = !DILocalVariable(name: "eth", scope: !57, file: !3, line: 125, type: !115)
!115 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !116, size: 64)
!116 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "ethhdr", file: !117, line: 159, size: 112, elements: !118)
!117 = !DIFile(filename: "/usr/include/linux/if_ether.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!118 = !{!119, !123, !124}
!119 = !DIDerivedType(tag: DW_TAG_member, name: "h_dest", scope: !116, file: !117, line: 160, baseType: !120, size: 48)
!120 = !DICompositeType(tag: DW_TAG_array_type, baseType: !79, size: 48, elements: !121)
!121 = !{!122}
!122 = !DISubrange(count: 6)
!123 = !DIDerivedType(tag: DW_TAG_member, name: "h_source", scope: !116, file: !117, line: 161, baseType: !120, size: 48, offset: 48)
!124 = !DIDerivedType(tag: DW_TAG_member, name: "h_proto", scope: !116, file: !117, line: 162, baseType: !86, size: 16, offset: 96)
!125 = !DILocalVariable(name: "____fmt", scope: !126, file: !3, line: 127, type: !129)
!126 = distinct !DILexicalBlock(scope: !127, file: !3, line: 127, column: 3)
!127 = distinct !DILexicalBlock(scope: !128, file: !3, line: 126, column: 44)
!128 = distinct !DILexicalBlock(scope: !57, file: !3, line: 126, column: 6)
!129 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 184, elements: !130)
!130 = !{!131}
!131 = !DISubrange(count: 23)
!132 = !DILocalVariable(name: "____fmt", scope: !133, file: !3, line: 129, type: !136)
!133 = distinct !DILexicalBlock(scope: !134, file: !3, line: 129, column: 4)
!134 = distinct !DILexicalBlock(scope: !135, file: !3, line: 128, column: 44)
!135 = distinct !DILexicalBlock(scope: !127, file: !3, line: 128, column: 6)
!136 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 160, elements: !137)
!137 = !{!138}
!138 = !DISubrange(count: 20)
!139 = !DILocalVariable(name: "____fmt", scope: !140, file: !3, line: 134, type: !143)
!140 = distinct !DILexicalBlock(scope: !141, file: !3, line: 134, column: 4)
!141 = distinct !DILexicalBlock(scope: !142, file: !3, line: 133, column: 48)
!142 = distinct !DILexicalBlock(scope: !127, file: !3, line: 133, column: 7)
!143 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 232, elements: !144)
!144 = !{!145}
!145 = !DISubrange(count: 29)
!146 = !DILocalVariable(name: "____fmt", scope: !147, file: !3, line: 139, type: !149)
!147 = distinct !DILexicalBlock(scope: !148, file: !3, line: 139, column: 4)
!148 = distinct !DILexicalBlock(scope: !142, file: !3, line: 138, column: 7)
!149 = !DICompositeType(tag: DW_TAG_array_type, baseType: !23, size: 176, elements: !150)
!150 = !{!151}
!151 = !DISubrange(count: 22)
!152 = !DILocation(line: 97, column: 37, scope: !57)
!153 = !DILocation(line: 99, column: 38, scope: !57)
!154 = !{!155, !156, i64 4}
!155 = !{!"xdp_md", !156, i64 0, !156, i64 4, !156, i64 8, !156, i64 12, !156, i64 16}
!156 = !{!"int", !157, i64 0}
!157 = !{!"omnipotent char", !158, i64 0}
!158 = !{!"Simple C/C++ TBAA"}
!159 = !DILocation(line: 99, column: 27, scope: !57)
!160 = !DILocation(line: 99, column: 19, scope: !57)
!161 = !DILocation(line: 99, column: 8, scope: !57)
!162 = !DILocation(line: 100, column: 34, scope: !57)
!163 = !{!155, !156, i64 0}
!164 = !DILocation(line: 100, column: 23, scope: !57)
!165 = !DILocation(line: 100, column: 15, scope: !57)
!166 = !DILocation(line: 100, column: 8, scope: !57)
!167 = !DILocation(line: 108, column: 8, scope: !57)
!168 = !DILocation(line: 111, column: 20, scope: !57)
!169 = !DILocation(line: 125, column: 17, scope: !57)
!170 = !DILocation(line: 126, column: 17, scope: !128)
!171 = !DILocation(line: 126, column: 32, scope: !128)
!172 = !DILocation(line: 126, column: 6, scope: !57)
!173 = !DILocation(line: 125, column: 23, scope: !57)
!174 = !DILocation(line: 127, column: 3, scope: !126)
!175 = !{!176, !177, i64 12}
!176 = !{!"ethhdr", !157, i64 0, !157, i64 6, !177, i64 12}
!177 = !{!"short", !157, i64 0}
!178 = !DILocation(line: 127, column: 3, scope: !127)
!179 = !DILocation(line: 128, column: 11, scope: !135)
!180 = !DILocation(line: 128, column: 19, scope: !135)
!181 = !DILocation(line: 128, column: 6, scope: !127)
!182 = !DILocation(line: 129, column: 4, scope: !133)
!183 = !DILocation(line: 129, column: 4, scope: !134)
!184 = !DILocation(line: 130, column: 25, scope: !134)
!185 = !DILocation(line: 102, column: 18, scope: !57)
!186 = !DILocation(line: 133, column: 19, scope: !142)
!187 = !DILocation(line: 133, column: 35, scope: !142)
!188 = !DILocation(line: 133, column: 7, scope: !127)
!189 = !DILocation(line: 134, column: 4, scope: !140)
!190 = !DILocation(line: 134, column: 4, scope: !141)
!191 = !DILocation(line: 24, column: 46, scope: !192, inlinedAt: !207)
!192 = distinct !DISubprogram(name: "xdp_stats_record_action", scope: !44, file: !44, line: 24, type: !193, isLocal: true, isDefinition: true, scopeLine: 25, flags: DIFlagPrototyped, isOptimized: true, unit: !2, variables: !195)
!193 = !DISubroutineType(types: !194)
!194 = !{!35, !60, !35}
!195 = !{!196, !197, !198}
!196 = !DILocalVariable(name: "ctx", arg: 1, scope: !192, file: !44, line: 24, type: !60)
!197 = !DILocalVariable(name: "action", arg: 2, scope: !192, file: !44, line: 24, type: !35)
!198 = !DILocalVariable(name: "rec", scope: !192, file: !44, line: 30, type: !199)
!199 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !200, size: 64)
!200 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "datarec", file: !201, line: 10, size: 128, elements: !202)
!201 = !DIFile(filename: "./../common/xdp_stats_kern_user.h", directory: "/home/ubuntu/EdgeComputingSlice/urllc/packet01-parsing")
!202 = !{!203, !206}
!203 = !DIDerivedType(tag: DW_TAG_member, name: "rx_packets", scope: !200, file: !201, line: 11, baseType: !204, size: 64)
!204 = !DIDerivedType(tag: DW_TAG_typedef, name: "__u64", file: !17, line: 31, baseType: !205)
!205 = !DIBasicType(name: "long long unsigned int", size: 64, encoding: DW_ATE_unsigned)
!206 = !DIDerivedType(tag: DW_TAG_member, name: "rx_bytes", scope: !200, file: !201, line: 12, baseType: !204, size: 64, offset: 64)
!207 = distinct !DILocation(line: 136, column: 11, scope: !141)
!208 = !DILocation(line: 24, column: 57, scope: !192, inlinedAt: !207)
!209 = !{!156, !156, i64 0}
!210 = !DILocation(line: 30, column: 24, scope: !192, inlinedAt: !207)
!211 = !DILocation(line: 30, column: 18, scope: !192, inlinedAt: !207)
!212 = !DILocation(line: 31, column: 7, scope: !213, inlinedAt: !207)
!213 = distinct !DILexicalBlock(scope: !192, file: !44, line: 31, column: 6)
!214 = !DILocation(line: 31, column: 6, scope: !192, inlinedAt: !207)
!215 = !DILocation(line: 38, column: 7, scope: !192, inlinedAt: !207)
!216 = !DILocation(line: 38, column: 17, scope: !192, inlinedAt: !207)
!217 = !{!218, !219, i64 0}
!218 = !{!"datarec", !219, i64 0, !219, i64 8}
!219 = !{!"long long", !157, i64 0}
!220 = !DILocation(line: 39, column: 25, scope: !192, inlinedAt: !207)
!221 = !DILocation(line: 39, column: 41, scope: !192, inlinedAt: !207)
!222 = !DILocation(line: 39, column: 34, scope: !192, inlinedAt: !207)
!223 = !DILocation(line: 39, column: 19, scope: !192, inlinedAt: !207)
!224 = !DILocation(line: 39, column: 7, scope: !192, inlinedAt: !207)
!225 = !DILocation(line: 39, column: 16, scope: !192, inlinedAt: !207)
!226 = !{!218, !219, i64 8}
!227 = !DILocation(line: 41, column: 9, scope: !192, inlinedAt: !207)
!228 = !DILocation(line: 41, column: 2, scope: !192, inlinedAt: !207)
!229 = !DILocation(line: 42, column: 1, scope: !192, inlinedAt: !207)
!230 = !DILocation(line: 136, column: 4, scope: !141)
!231 = !DILocation(line: 139, column: 4, scope: !147)
!232 = !DILocation(line: 139, column: 4, scope: !148)
!233 = !DILocation(line: 140, column: 4, scope: !148)
!234 = !DILocation(line: 24, column: 46, scope: !192, inlinedAt: !235)
!235 = distinct !DILocation(line: 156, column: 9, scope: !57)
!236 = !DILocation(line: 24, column: 57, scope: !192, inlinedAt: !235)
!237 = !DILocation(line: 30, column: 24, scope: !192, inlinedAt: !235)
!238 = !DILocation(line: 30, column: 18, scope: !192, inlinedAt: !235)
!239 = !DILocation(line: 31, column: 7, scope: !213, inlinedAt: !235)
!240 = !DILocation(line: 31, column: 6, scope: !192, inlinedAt: !235)
!241 = !DILocation(line: 38, column: 7, scope: !192, inlinedAt: !235)
!242 = !DILocation(line: 38, column: 17, scope: !192, inlinedAt: !235)
!243 = !DILocation(line: 39, column: 25, scope: !192, inlinedAt: !235)
!244 = !DILocation(line: 39, column: 41, scope: !192, inlinedAt: !235)
!245 = !DILocation(line: 39, column: 34, scope: !192, inlinedAt: !235)
!246 = !DILocation(line: 39, column: 19, scope: !192, inlinedAt: !235)
!247 = !DILocation(line: 39, column: 7, scope: !192, inlinedAt: !235)
!248 = !DILocation(line: 39, column: 16, scope: !192, inlinedAt: !235)
!249 = !DILocation(line: 41, column: 9, scope: !192, inlinedAt: !235)
!250 = !DILocation(line: 41, column: 2, scope: !192, inlinedAt: !235)
!251 = !DILocation(line: 42, column: 1, scope: !192, inlinedAt: !235)
!252 = !DILocation(line: 156, column: 2, scope: !57)
!253 = !DILocation(line: 157, column: 1, scope: !57)
