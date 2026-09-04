#!/bin/sh
# index.html の JSON-LD "dateModified" と sitemap.xml の <lastmod> を、指定日（省略時は今日）にそろえる。
#
#   使い方:  tools/stamp-dates.sh              今日の日付にする
#            tools/stamp-dates.sh 2026-09-04   日付を指定する
#            tools/stamp-dates.sh --staged     .git/hooks/pre-commit から呼ぶ用。
#                                              index.html か sitemap.xml が staged のときだけ動き、
#                                              staged の中身と作業ツリーの両方の日付を書き換える
#                                              （作業ツリーの他の未 staged の変更は巻き込まない）。
set -e
cd "$(dirname "$0")/.."
staged=0; day=""
for a in "$@"; do case "$a" in --staged) staged=1;; *) day="$a";; esac; done
[ -n "$day" ] || day=$(date +%F)
case "$day" in [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;; *) echo "日付の形式が違う: $day" >&2; exit 1;; esac

E_HTML="s/(\"dateModified\": *\")[0-9]{4}-[0-9]{2}-[0-9]{2}(\")/\1$day\2/"
E_XML="s#(<lastmod>)[0-9]{4}-[0-9]{2}-[0-9]{2}(</lastmod>)#\1$day\2#"

if [ $staged -eq 1 ]; then
  git diff --cached --name-only | grep -qx -e index.html -e sitemap.xml || exit 0
  for f in index.html sitemap.xml; do
    case $f in index.html) e=$E_HTML;; *) e=$E_XML;; esac
    blob=$(git show ":$f" | sed -E "$e" | git hash-object -w --stdin)
    git update-index --cacheinfo "100644,$blob,$f"
  done
fi
sed -i '' -E "$E_HTML" index.html
sed -i '' -E "$E_XML" sitemap.xml
echo "dateModified / lastmod -> $day"
