#!/usr/bin/env bash
# 将 docs/issues/ 下的 5 个 issue 草稿发布到 GitHub 仓库。
#
# 当前 gh 使用的 fine-grained PAT 没有对他人仓库的 issue 写权限，
# 先执行以下任一操作后再运行本脚本：
#   gh auth refresh -h github.com -s public_repo   # 或
#   gh auth login                                   # 重新用浏览器授权
set -euo pipefail

REPO="jeams11/AI-News-Agent"
DIR="$(cd "$(dirname "$0")" && pwd)"

for file in "$DIR"/0*.md; do
    # 第一行 "# 标题" 作为 issue 标题，其余作为正文
    title="$(head -1 "$file" | sed 's/^# //')"
    body="$(tail -n +2 "$file")"
    echo "创建 issue: $title"
    gh issue create -R "$REPO" --title "$title" --body "$body"
done

echo "全部完成"
