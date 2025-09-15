#!/bin/bash
# 実行場所は models/ 直下を想定
# ycb_* ディレクトリを探索して dae/sdf 内の識別子をリネーム

set -e

for d in ycb_*; do
    [ -d "$d" ] || continue

    echo "Processing $d ..."
    texdir="$d/materials/textures"

    # ディレクトリ作成
    mkdir -p "$texdir"

    # テクスチャ画像移動＆リネーム
    if [ -f "$d/meshes/texture_map.png" ]; then
        mv "$d/meshes/texture_map.png" "$texdir/${d}.png"
    fi

    # STL リネーム
    if [ -f "$d/meshes/nontextured.stl" ]; then
        mv "$d/meshes/nontextured.stl" "$d/meshes/${d}.stl"
    fi

    # DAE リネーム
    if [ -f "$d/meshes/textured.dae" ]; then
        mv "$d/meshes/textured.dae" "$d/meshes/${d}.dae"
    fi

    # DAE 内の置換
    dae_file="$d/meshes/${d}.dae"
    if [ -f "$dae_file" ]; then
        sed -i \
        -e "s/texture0/texture_${d}_png/g" \
        -e "s/material0-fx/material_${d}-fx/g" \
        -e "s/material0/material_${d}/g" \
        -e "s/shape0-lib/shape_${d}-lib/g" \
        -e "s/shape0/shape_${d}/g" \
        -e "s#<init_from>.*\.png</init_from>#<init_from>../materials/textures/${d}.png</init_from>#g" \
        "$dae_file"
    fi

    # SDF 内の置換
    sdf_file="$d/model-1_4.sdf"
    if [ -f "$sdf_file" ]; then
        sed -i \
        -e "s#model://$d/meshes/textured.dae#model://$d/meshes/${d}.dae#g" \
        -e "s#model://$d/meshes/nontextured.stl#model://$d/meshes/${d}.stl#g" \
        "$sdf_file"
    fi

    echo "Done $d"
done

echo "All ycb_* models processed."
