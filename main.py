from PyPDF2 import PaperSize, PdfReader
import configparser
#config_ini.get('MYSQL', 'pass')
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

print("-------------------------------------------------------------")

with open("aa.pdf", "rb") as input:
    reader = PdfReader(input)
    page = reader.pages[0] 

    # 読み込んだページのテキストを抽出
    paper = page.extract_text()
    
    # 所属のデータを抽出
    aff_start_index = paper.index('入学') + 3  # 最初の'['の位置を特定し、次の文字の位置を取得
    aff_end_index = paper[aff_start_index:].index('\n') + aff_start_index
    aff = paper[aff_start_index:aff_end_index]
    print(aff)
    

    #print(p_2) #≪から先
    count_lines = p_2.count('\n') + 1
    #print(count_lines) #行数

    sub_list = p_2.splitlines()
    #print(sub_list) #全ての行を1行毎、配列の要素として格納した配列
    #print(sub_list[1]) 

    print(sub_list[43])
    tmp = sub_list[43].removeprefix("  ")
    # print(tmp)
    tmp_2 = (tmp[7:])
    # print(tmp_2)
    sep = ' '
    t = tmp_2.split(sep)
    # print(t)
    back_sub = "  "+t[2]+"  "+t[4]+" "+t[5]
    # print(back_sub) #後ろの科目完成
    front_sub = sub_list[43].replace(back_sub,"")
    sub_list[43] = front_sub
    # print(len(sub_list))
    sub_list[44:44] = [back_sub]
    # print(len(sub_list))
    # print(sub_list)

    # 特定の含む要素のインデックスを取得する
    title_indices = [i for i, s in enumerate(sub_list) if '≪' in s]
    print(title_indices)

    title_list = []
    
    for i in title_indices:
        title_list.append(sub_list[i])

    print(title_list)

    hissyuu_list = []
    sentaku_list = []
    kisokyou_tagakubu_list = []
    kisokyou_list = []
    dounyuu_list = []
    eigo_list = []
    gaikokugo_list = []

    def data_list_cre(title, sub_list):
        if title in sub_list:
            title_index = sub_list.index(title)
            hi_i = title_indices.index(title_index)
            next_index = 0
            if hi_i+1 != len(title_indices):
                next_index = title_indices[hi_i + 1]
            else :
                next_index = len(sub_list)
            for i in range(title_index+1,next_index):
                subInfo_list = sub_list[i].split(sep)
                subInfo_list_2 = []
                subInfo_list_2.append(subInfo_list[2])
                year = subInfo_list[4][0:2]
                grade = subInfo_list[4].replace(year,'')
                subInfo_list_2.append(year)
                subInfo_list_2.append(grade)
                subInfo_list_2.append(subInfo_list[5])
                if '認' in subInfo_list_2[2]:
                    subInfo_list_2.append('認定') 
                elif '☆' in subInfo_list_2[2]:
                    subInfo_list_2.append('履修中') 
                else :
                    subInfo_list_2.append('') 
                sub_list.append(subInfo_list_2)
                #print(subInfo_list_2)
        #print('')
    
    data_list_cre(title_list[0], hissyuu_list)
    data_list_cre(title_list[1], sentaku_list)
    data_list_cre(title_list[2], kisokyou_tagakubu_list)
    data_list_cre(title_list[3], kisokyou_list)
    data_list_cre(title_list[4], dounyuu_list)
    data_list_cre(title_list[5], eigo_list)
    data_list_cre(title_list[6], gaikokugo_list)
    
    tanni_sum = 0
    gp_sum = 0

    gp_dic = {'E':0, 'D':0, 'C':1, 'B':2, 'A':3, 'S':4}

    def add_tanni(sub_list, tanni_sum):
        if sub_list != []: #リストに何か追加されているとき
            for i in range(len(sub_list)):
                if sub_list[i][4] == '' :
                    tanni_sum += int(sub_list[i][0])
        return tanni_sum
        

    tanni_sum = add_tanni(hissyuu_list, tanni_sum)
    tanni_sum = add_tanni(sentaku_list, tanni_sum)
    tanni_sum = add_tanni(kisokyou_tagakubu_list, tanni_sum)
    tanni_sum = add_tanni(kisokyou_list, tanni_sum)
    tanni_sum = add_tanni(dounyuu_list, tanni_sum)
    tanni_sum = add_tanni(eigo_list, tanni_sum)
    tanni_sum = add_tanni(gaikokugo_list, tanni_sum)

    def add_gp(sub_list, gp_sum):
        if sub_list != []: #リストに何か追加されているとき
            for i in range(len(sub_list)):
                if sub_list[i][4] == '' :
                    gp_sum += int(sub_list[i][0])*gp_dic[sub_list[i][2]]
        return gp_sum

    gp_sum = add_gp(hissyuu_list, gp_sum)
    gp_sum = add_gp(sentaku_list, gp_sum)
    gp_sum = add_gp(kisokyou_tagakubu_list, gp_sum)
    gp_sum = add_gp(kisokyou_list, gp_sum)
    gp_sum = add_gp(dounyuu_list, gp_sum)
    gp_sum = add_gp(eigo_list, gp_sum)
    gp_sum = add_gp(gaikokugo_list, gp_sum)
    print(gp_sum, tanni_sum)
    
    
    gpa = gp_sum / tanni_sum
    print(gpa) 


