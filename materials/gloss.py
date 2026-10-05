"""Add "(pinyin, English)" after every bare Chinese term on a course page.

The house rule: a Chinese term on an English page carries its English in brackets, every
occurrence. This adds the gloss where a term is not already followed by a bracket, using the
word list below, and REPORTS any term it does not know instead of guessing. Text inside <script>,
<style> and tag attributes is left alone. Usage:
    python3 gloss.py <page.html> [--write]
The word list is shared by both Business Chinese courses: the Advanced course imports this file.
"""
import re
import sys

GLOSS = {
    # session 1 and the trainer's phrase list
    "买": ("mǎi", "buy"), "卖": ("mài", "sell"), "买卖": ("mǎimài", "business, buying and selling"),
    "你好": ("nǐ hǎo", "hello"), "您好": ("nín hǎo", "hello, polite"), "开会": ("kāihuì", "have a meeting"),
    "经理": ("jīnglǐ", "manager"), "老板": ("lǎobǎn", "boss, owner"), "不是": ("bú shì", "is not"),
    "一定": ("yídìng", "certainly"), "一起": ("yìqǐ", "together"), "合同": ("hétong", "contract"),
    "价格": ("jiàgé", "price"), "公司": ("gōngsī", "company"), "不": ("bù", "not"), "一": ("yī", "one"),
    "你": ("nǐ", "you"), "好": ("hǎo", "good"), "很好": ("hěn hǎo", "very good"), "不好": ("bù hǎo", "not good"),
    "不要": ("bú yào", "do not want"), "第一": ("dì yī", "first"), "怪": ("guài", "strange"), "贵": ("guì", "expensive"),
    "安": ("ān", "safe"), "钱": ("qián", "money"), "谢谢": ("xièxie", "thank you"), "菜": ("cài", "dish"),
    "在": ("zài", "at, be in"), "去": ("qù", "go"), "十": ("shí", "ten"), "四": ("sì", "four"),
    "是": ("shì", "to be, yes"), "请": ("qǐng", "please, invite"), "轻": ("qīng", "light in weight"),
    "桌子": ("zhuōzi", "table"), "吗": ("ma", "question particle"), "妈": ("mā", "mother"), "麻": ("má", "hemp, numb"),
    "马": ("mǎ", "horse"), "骂": ("mà", "scold"), "鲁门物流": ("Lǔmén Wùliú", "Lumen Logistics"),
    "我们想买": ("wǒmen xiǎng mǎi", "we want to buy"), "王总": ("Wáng zǒng", "President Wang"),
    "王经理": ("Wáng jīnglǐ", "Manager Wang"), "李经理": ("Lǐ jīnglǐ", "Manager Li"),
    "麻烦": ("máfan", "may I trouble you"), "万": ("wàn", "ten thousand"),
    "汉语拼音方案": ("Hànyǔ Pīnyīn Fāng'àn", "the Scheme for the Chinese Phonetic Alphabet"),
    "您": ("nín", "you, polite"), "子": ("zi", "noun suffix"), "很": ("hěn", "very"), "谢": ("xiè", "thank"),
    # Advanced: register and formal writing
    "贵公司": ("guì gōngsī", "your company, polite"), "贵司": ("guì sī", "your company, polite"), "我司": ("wǒ sī", "our company, formal"),
    "你们公司": ("nǐmen gōngsī", "your company, casual"), "我们公司": ("wǒmen gōngsī", "our company, casual"),
    "烦请": ("fánqǐng", "may I trouble you to"), "请查收": ("qǐng cháshōu", "please find attached"),
    "如有疑问": ("rú yǒu yíwèn", "if you have any questions"), "是否": ("shìfǒu", "whether, formal"),
    "尊敬的": ("zūnjìng de", "dear, respected"), "此致": ("cǐzhì", "with this I convey"), "敬礼": ("jìnglǐ", "respects"),
    "此致 敬礼": ("cǐzhì jìnglǐ", "with respect"), "顺颂商祺": ("shùn sòng shāng qí", "wishing your business well, classical"),
    "敝司": ("bì sī", "our humble company, classical"), "鄙人": ("bǐrén", "this humble person, classical"),
    "兹": ("zī", "hereby, classical"), "谨此": ("jǐn cǐ", "respectfully hereby"), "承蒙": ("chéngméng", "indebted to, classical"),
    "恭候佳音": ("gōnghòu jiāyīn", "awaiting your good news, classical"), "哈哈": ("hāha", "ha ha"),
    "嗯嗯": ("ńg ńg", "mm-hm"), "亲": ("qīn", "dear, shop-assistant style"), "啦": ("la", "casual particle"),
    "哦": ("o", "casual particle"), "吧": ("ba", "suggestion particle"), "咋样": ("zǎyàng", "how about it, casual"),
    "搞定": ("gǎodìng", "sorted, casual"), "回头": ("huítóu", "later, casual"), "赶紧": ("gǎnjǐn", "hurry, casual"),
    "帮我": ("bāng wǒ", "help me"), "谢啦": ("xiè la", "thanks, casual"), "没问题": ("méi wèntí", "no problem"),
    "王经理您好": ("Wáng jīnglǐ nín hǎo", "hello, Manager Wang"), "你可以": ("nǐ kěyǐ", "you can"), "烦请您": ("fánqǐng nín", "may I trouble you"),
    "同比": ("tóngbǐ", "year on year"), "环比": ("huánbǐ", "period on period"), "面子": ("miànzi", "face"),
    "我们研究一下": ("wǒmen yánjiū yíxià", "we will look into it"), "微信": ("Wēixìn", "WeChat"),
    "感谢": ("gǎnxiè", "thank"), "稍后": ("shāohòu", "later, formal"), "尽快": ("jǐnkuài", "as soon as possible"),
    "敬酒": ("jìngjiǔ", "propose a toast"), "客气": ("kèqi", "polite, standing on ceremony"),
}
H = "㐀-䶿一-鿿"
# the same term pattern as course-builder/scripts/pre-publish.py's CJK check (one reader, one rule):
# a term may contain digits, spaces and CJK punctuation between characters, so 此致 敬礼 is one term
TERM = re.compile("[" + H + "](?:[" + H + "0-9.%~ \\-\u00b7\u3001\uff0c]*[" + H + "])?")
FOLLOWED = re.compile(r"\s*[(（]\s*[A-Za-zÀ-ɏ]")


def gloss_text(t, unknown):
    out, last = [], 0
    for m in TERM.finditer(t):
        out.append(t[last:m.end()])
        last = m.end()
        if FOLLOWED.match(t[m.end():m.end() + 12]):
            continue
        g = GLOSS.get(m.group(0))
        if g is None:
            unknown.add(m.group(0))
            continue
        out.append(f" ({g[0]}, {g[1]})")
    out.append(t[last:])
    return "".join(out)


def gloss_page(html):
    unknown = set()
    # SVG is protected: a bracket appended inside a figure label breaks its geometry, so figure
    # labels are restructured by hand (the next label starts with "(pinyin, English)")
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<[^>]+>)", html, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = gloss_text(parts[i], unknown)
    return "".join(parts), unknown


if __name__ == "__main__":
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    new, unknown = gloss_page(src)
    added = new.count("(") - src.count("(")
    print(f"{path.split('/')[-1]}: {added} glosses added; unknown terms: {sorted(unknown) or 'none'}")
    svg_bare = []
    for blk in re.findall(r"<svg\b.*?</svg>", src, flags=re.S):
        flat = re.sub(r"<[^>]+>", " ", blk)
        flat = re.sub(r"aria-label=\"[^\"]*\"", "", flat)
        for m in TERM.finditer(flat):
            if not FOLLOWED.match(flat[m.end():m.end() + 12]):
                svg_bare.append(m.group(0) + " -> " + flat[m.end():m.end() + 18].strip())
    print("figure labels to restructure by hand:", svg_bare or "none")
    if "--write" in sys.argv and not unknown:
        open(path, "w", encoding="utf-8").write(new)
        print("written")
    elif "--write" in sys.argv:
        print("NOT written: add the unknown terms to GLOSS first")
