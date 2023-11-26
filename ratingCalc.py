import json
import functools
import colorama


colorama.init()

MAG = colorama.Fore.MAGENTA
YEL = colorama.Fore.YELLOW
CYA = colorama.Fore.CYAN
GRY = colorama.Fore.LIGHTBLACK_EX
BYEL = colorama.Fore.LIGHTYELLOW_EX
RST = colorama.Fore.RESET
RED = colorama.Fore.RED
GRE = colorama.Fore.GREEN
BLU = colorama.Fore.BLUE
WHT = colorama.Fore.WHITE


def singleRating(dif, score):
    """根据定数和分数计算Rating

    Args:
        dif (float): 谱面定数
        score (int): 谱面分数

    Returns:
        float: Rating
    """
    if score > 1008000:
        return dif + 3.4 + (score - 1008000) / 10000
    elif score > 1004000:
        return dif + 2.4 + (score - 1004000) / 4000
    elif score > 1000000:
        return dif + 2 + (score - 1000000) / 10000
    elif score > 980000:
        return dif + 1 + (score - 980000) / 20000
    elif score > 950000:
        return dif + (score - 950000) / 30000
    elif score > 900000:
        return dif - 1 + (score - 900000) / 50000
    elif score > 500000:
        return dif - 5 + (score - 500000) / 100000
    else:
        return 0


def readCache() -> dict:
    """读取本地个人全曲信息

    Returns:
        dict: 全曲信息json
    """
    file = open("res.json", "r", encoding="utf-8")
    str = file.read()
    data = json.loads(str)
    file.close()
    return data


def difRead() -> dict:
    """从本地文件读取信息

    Returns:
        dcit: 信息列表
    """
    file = open(
        rf"wiki_songlist.json",
        "r",
        encoding="utf-8",
    )
    str = file.read()
    data = json.loads(str)
    file.close()
    return data


def num2rm(num: int) -> str:
    """阿拉伯数字转罗马数字

    Args:
        num (int): 阿拉伯数字

    Returns:
        str: 罗马数字(I,II,III,IV)
    """
    if num == 1:
        return "I"
    elif num == 2:
        return "II"
    elif num == 3:
        return "III"
    elif num == 4:
        return "IV"
    else:
        raise (Exception("阿拉伯数字数字转罗马(num2rm): num 必须为 1,2,3,4"))


def difInit() -> dict:
    """难度初始化

    返回一个字典，键为song_id，值为四个定数和歌曲名字组成的字典
    """
    difDic = {}
    songDif = difRead()["songs"]
    for song in songDif:
        difDic[song["id"]] = {}
        for i in range(4):
            difDic[song["id"]][num2rm(i + 1)] = song["difficulties"][i]["ratingReal"]
        difDic[song["id"]]["name"] = song["title_localized"]["default"]
    return difDic


def nameInit():
    """name2id的初始化
    会在根目录存储一个json文件

    """
    nameDic = {}
    songDif = difRead()["songs"]
    for song in songDif:
        nameDic[song["title_localized"]["default"]] = song["id"]
    dicText = json.dumps(nameDic)
    file = open(
        "miho_nt/plugins/Rotaeno_Functions_Collections/untils/name2id.json", "w"
    )
    file.write(dicText)
    file.close()
    # 吃完了


def name2id(name: str) -> str:
    """查询name对应的song_id

    Args:
        name (str): 歌曲名字

    Returns:
        str: song_id
    """
    file = open(
        "miho_nt/plugins/Rotaeno_Functions_Collections/untils/name2id.json", "r"
    )
    jsonName = json.load(file)
    file.close()
    return jsonName[id]


def ratingCalc(id: str, score: list, flag: list, clear: list) -> list:
    """计算单曲Rating

    Args:
        id (str): 歌曲id
        score (list): 4个难度的谱面分数
        flag (str): 谱面状态
        clear (bool): 通过状态

    返回一个songList，包含4个难度谱面的rating和各个状态
    """
    difDic = difInit()
    songBest = []
    for i in range(4):
        songArg = (
            singleRating(difDic[id][num2rm(i + 1)], score[i]),
            id,
            num2rm(i + 1),
            difDic[id][num2rm(i + 1)],
            flag[i],
            clear[i],
            difDic[id]["name"],
            score[i],
        )
        songBest.append(songArg)
    return songBest


def cmp1(a: list, b: list):
    return (a[0] < b[0]) - (a[0] > b[0])


def cmp2(a: list, b: list):
    return (a[0] < b[0]) - (a[0] > b[0])


def difColor(dif: str) -> str:
    """根据谱面难度输出颜色

    Args:
        dif (str): 难度(I,II,III,IV)

    Returns:
        str: 颜色(colorama)
    """
    if dif == "I":
        return GRE
    if dif == "II":
        return YEL
    if dif == "III":
        return BLU
    if dif == "IV":
        return RED
    return WHT


def clearColor(clear: bool) -> str:
    """根据通过情况输出颜色

    Args:
        clear (bool): 通过情况

    Returns:
        str: 颜色(colorama)
    """
    if clear == True:
        return GRE
    else:
        return RED


def flagColor(flag: str) -> str:
    """根据成绩情况输出颜色

    Args:
        flag (str): 成绩情况

    Returns:
        str: 颜色(colorama)
    """
    if flag == "AP":
        return BYEL
    if flag == "FC":
        return BLU
    if flag == "CL":
        return GRE
    if flag == "FL":
        return GRY
    return WHT


def ratingVisualize(songBest: list, songRecent: list, difDic: dict):
    """个人Rating可视化

    Args:
        songBest (list): 个人Best(允许无序)
        songRecent (list): 个人Recent(允许无序)
    """
    sortedList = sorted(songBest, key=functools.cmp_to_key(cmp1))
    Sum1 = 0
    Sum2 = 0
    Sum3 = 0
    bestList = []
    recentList = []
    for i in range(len(sortedList)):
        if i < 10:
            bestList.append(sortedList[i])
            Sum1 += sortedList[i][0]
        elif i < 30:
            bestList.append(sortedList[i])
            Sum2 += sortedList[i][0]
        else:
            break
    sortedRecords = sorted(songRecent, key=functools.cmp_to_key(cmp2))
    for i in range(len(sortedRecords)):
        if i == 10:
            break
        recentList.append(sortedRecords[i])
        Sum3 += sortedRecords[i][0]
    rating = (Sum1 * 0.07 + Sum2 * 0.015) * 0.75 + Sum3 * 0.025
    print(f"Your rating is {colorama.Fore.MAGENTA}{'%3f'%rating}{colorama.Fore.RESET}")
    print(f"The followings are your B30: ")
    for i in range(len(sortedList)):
        if i == 30:
            break
        id = sortedList[i][1]
        dif = sortedList[i][2]
        level = "%.1f" % sortedList[i][3]
        rating = "%.3f" % sortedList[i][0]
        flag = sortedList[i][4]
        clear = sortedList[i][5]
        if flag == "NONE":
            if clear:
                flag = "CL"
            else:
                flag = "FL"
        if i < 10:
            print(
                f"{WHT}No. {YEL}{i+1:<2} {WHT} {difDic[id]['name']}, Dif: {difColor(dif)}{level:}{WHT}, Rating: {YEL}{rating}{WHT}, Status: {flagColor(flag)}{flag}{RST}, Clear: {clearColor(clear)}{clear}{RST}"
            )
        else:
            print(
                f"{WHT}No. {i+1:<2} {WHT} {difDic[id]['name']}, Dif: {difColor(dif)}{level:}{WHT}, Rating: {YEL}{rating}{RST}, Status: {flagColor(flag)}{flag}{RST}, Clear: {clearColor(clear)}{clear}{RST}"
            )
    print(f"The followings are your R10: ")
    for i in range(len(sortedRecords)):
        if i >= 10:
            break
        print(
            f"{WHT}No. {YEL}{i+1:<2} {WHT} Dif: {difColor(sortedRecords[i][2])}{'%.1f'%sortedRecords[i][3]}{WHT}, Rating: {YEL}{'%.3f'%sortedRecords[i][0]}{RST}"
        )


def ratingB3R1(songBest: list, songRecent: list) -> tuple:
    """根据个人Best和Recent得到总Rating以及B30和R10

    如果Best或Recent数量不足则会返回原本数量的list

    Args:
        songBest (list): 个人Best(允许无序)
        songRecent (list): 个人Recent(允许无序)

    Returns:
        tuple: 由总Rating和B30,R10组成的元组
    """
    sortedList = sorted(songBest, key=functools.cmp_to_key(cmp1))
    Sum1 = 0
    Sum2 = 0
    Sum3 = 0
    bestList = []
    recentList = []
    for i in range(len(sortedList)):
        if i < 10:
            bestList.append(sortedList[i])
            Sum1 += sortedList[i][0]
        elif i < 30:
            bestList.append(sortedList[i])
            Sum2 += sortedList[i][0]
        else:
            break
    sortedRecords = sorted(songRecent, key=functools.cmp_to_key(cmp2))
    for i in range(len(sortedRecords)):
        if i == 10:
            break
        recentList.append(sortedRecords[i])
        Sum3 += sortedRecords[i][0]
    rating = (Sum1 * 0.07 + Sum2 * 0.015) * 0.75 + Sum3 * 0.025
    return (rating, bestList, recentList)


def recordProc(recentText: str, recentRating: float, difDic: dict) -> list:
    """根据单条Recent记录输出单条Recent信息

    Args:
        recentText (str): Recent信息
        recentRating (float): RecentRating
        difDic (dict): Dif字典


    Returns:
        list: 单条Recnet信息
    """
    songRecent = []
    pos = recentText.find("[")
    dif = recentText[pos + 1 : -1].upper()
    id = recentText[: pos - 1]
    songRecent.append((recentRating, id, dif, difDic[id][dif]))
    return songRecent


def songFind(songId: str, songList: list, dif: str = "-") -> list:
    """歌曲信息查找

    Args:
        songId (str): 希望找到的歌曲的id
        songList (list): 总歌曲列表
        dif (str, optional): 希望获取的难度. 默认为"-"(所有).

    Returns:
        list: 找到的歌曲信息，
    """
    songDif = []
    for song in songList:
        if song[1] == songId:
            print(song)
            if (dif == "-") or (song[2] == dif):
                songDif.append(song)
    return songDif


def ratingGet(jsonData: dict, flag: bool = False) -> tuple:
    """根据个人全曲信息计算Rating,B30和R10

    Args:
        jsonData (dict): 个人全曲信息
        flag (bool): 默认False输出全部信息，True输出B30和R10

    Returns:
        tuple: 一个包含总Rating,B30和R10的元组
    """
    songScores = jsonData["results"][0]["cloudSave"]["data"]["data"]["songs"]["songs"]
    songRecs = jsonData["results"][0]["cloudSave"]["data"]["data"]["playRecords"][
        "RecentRatingEntries"
    ]
    difDic = difInit()
    songRecent = []
    songBest = []
    for rec in songRecs:
        songRecent += recordProc(rec["ChartId"], rec["PlayRating"], difDic)
    for songId in songScores.keys():
        singleSong = songScores[songId]
        scores = []
        flags = []
        clears = []
        for i in range(4):
            scores.append(singleSong["levels"][num2rm(i + 1)]["Score"])
            flags.append(singleSong["levels"][num2rm(i + 1)]["Flag"])
            clears.append(singleSong["levels"][num2rm(i + 1)]["IsCleared"])
        songBest += ratingCalc(songId, scores, flags, clears)
    # ratingVisualize(songBest, songRecent, difDic)
    if flag:
        return ratingB3R1(songBest, songRecent)
    else:
        return (ratingB3R1(songBest, songRecent)[0], songBest, songRecent)


jsonData = readCache()
print(ratingGet(jsonData, True)[1])
