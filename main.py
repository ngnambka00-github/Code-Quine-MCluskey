import itertools as it

# File MyClass.py
# PhanTu là đối tượng để chứa chỉ số mintern, maxtern hoặc don't care  
# Và mã nhị phân tương ứng dạng chuỗi và mã Code(A, B, A', B',...)
class PhanTu: 
    def __init__(self, so_bien, chi_so):
        self.__so_bien = so_bien
        self.__chi_so = [x for x in chi_so]

    # chuyển chỉ số sang mã nhị phân 
    @property
    def code_binary(self):
        if (len(self.__chi_so) > 1): return None 
        str_format = "{0:>0" + str(self.__so_bien) + "s}"
        return str_format.format(bin(int(self.__chi_so[0]))[2:])
        
    # chuyển mã nhị phấn sang kí tự (A, B, A', B',...) dạng mintern
    @property
    def code_mintern(self):
        arr = [chr(ord('A')+i)for i in range(self.__so_bien)]
        arr_code = ''
        binary = self.__ma_nhi_phan
        for i in range(len(binary)):
            if binary[i] != '-':
                if binary[i] == '1': 
                    arr_code += arr[i]
                else: 
                    arr_code += arr[i]+"\'"
        return arr_code

    # chuyển mã nhị phấn sang kí tự (A, B, A', B',...) dạng maxtern 
    @property
    def code_maxtern(self):
        arr = [chr(ord('A')+i)for i in range(self.__so_bien)]
        arr_code = '('
        binary = self.__ma_nhi_phan
        for i in range(len(binary)):
            if binary[i] != '-':
                if binary[i] == '0':
                    arr_code += arr[i]+" + "
                else: 
                    arr_code += arr[i]+"\' + "
        arr_code = arr_code[0:len(arr_code)-3]+")"
        return arr_code 

    @property # Đếm số lượng bit 1 
    def count_bit_one(self):
        return self.__ma_nhi_phan.count('1')

    # Check xem 2 nhóm có khác nhau duy nhất 1 bit hay không
    def check_khac_nhau_1_bit(self, n2):
        ma1 = self.__ma_nhi_phan
        ma2 = n2.__ma_nhi_phan
        count = 0
        for i in range(len(ma1)):
            count += (1 if ma1[i] != ma2[i] else 0)
        return count == 1

    @property # Getter chỉ số
    def p_chi_so(self): return self.__chi_so

    @property # Getter số biến
    def p_so_bien(self): return self.__so_bien

    @property # Getter mã nhị phân
    def p_ma_nhi_phan(self): return self.__ma_nhi_phan
    
    @p_ma_nhi_phan.setter # Setter mã nhị phân
    def p_ma_nhi_phan(self, ma_nhi_phan):
        self.__ma_nhi_phan = ma_nhi_phan 

    # hàm so sánh 2 nhóm (bằng nhau khi có mã nhị phân giống nhau)
    def __eq__(self, other):
        return self.__ma_nhi_phan == other.__ma_nhi_phan
    
    # Hàm hủy bộ nhớ các biến
    def __del__(self):
        del self.__chi_so, self.__ma_nhi_phan, self.__so_bien


# File MyFunction.py
# Trả về mã nhị phân mới khi 2 nhóm khác nhau duy nhất 1 bit
def ma_nhi_phan_moi(ma1, ma2):
    ma = ''
    for i in range(len(ma1)):
        ma += (ma1[i] if ma1[i]==ma2[i] else '-')
    return ma

# Hàm kiểm tra có tồn tại phần tử trong mảng 
def add_khong_trung(arr, *item):
    if len(arr) == 0:
        for x in item: arr.append(x)
    else:
        for x in item: 
            if arr.count(x) == 0: arr.append(x)

# Hàm kiểm tra có tồn tại phần tử trong mảng hay không
def check_ton_tai(arr, item): 
    if len(arr) == 0: return False 
    return True if arr.count(item) > 0 else False

# Hàm thực hiện tổ hợp các nhóm lại,
# Loại bỏ nhóm trùng và lấy danh sách các nhóm có độ dài ngắn nhất 
def to_hop_nhom(arr_temp):
    min_length = len(arr_temp)
    arr_tron = []
    arr_so_luong_moi_hang = []
    arr_choice = [0]*len(arr_temp)
    so_lan_lap = 1
    for i in range(len(arr_temp)):
        so_lan_lap *= len(arr_temp[i])
        arr_so_luong_moi_hang.append(len(arr_temp[i]))
    
    index = 0
    while index < so_lan_lap:
        arr_row = []
        for i in range(len(arr_temp)):
            add_khong_trung(arr_row, arr_temp[i][arr_choice[i]])
        index += 1 
        check_nho = True 
        for i in range(len(arr_temp)-1, -1, -1):
            arr_choice[i] += 1
            if arr_choice[i] == arr_so_luong_moi_hang[i]:
                arr_choice[i] = 0
            else: 
                check_nho = False
        if len(arr_row) < min_length:
            min_length = len(arr_row)
        arr_tron.append(arr_row)
    return [x for x in arr_tron if min_length == len(x)]

class XuLy:
    # arr truyền vào là mintern
    def __init__(self, so_bien, arr, arr_dont_care):
        arr_join = sorted(arr+arr_dont_care)
        self.mintern = arr 
        self.so_bien = so_bien
        arr = []
        for item in arr_join: 
            item = [item]
            n = PhanTu(so_bien, item)
            n.p_ma_nhi_phan = n.code_binary
            arr.append(n)
        self.arr_nhom = arr
    
    # Hàm trả về mảng mà số lượng bít 1 chung 1 nhóm 
    # Và được SX theo số lượng bit 1 tăng dần 
    def arr_theo_sl_bit_1(self):
        arr = []
        for i in range(self.so_bien+1):
            arr_tmp=[x for x in self.arr_nhom if x.count_bit_one==i]
            arr.append(arr_tmp)
        # chuyển mảng 2 chiều về 1 chiều
        return list(it.chain.from_iterable(arr))  

    # Hàm trả về các Prime Implicant (PI)
    def arr_prime_implicant(self):
        arr_all = self.arr_nhom.copy()
        arr_pi = [] # Chứa các phần tử không có cặp 
        arr_co_cap = []
        arr_new = []
        while True: 
            check = False
            size = len(arr_all)
            for i in range(size-1):
                dem = 0
                nhom_A = arr_all[i]
                for j in range(i+1, size):
                    nhom_B = arr_all[j]
                    if nhom_A.check_khac_nhau_1_bit(nhom_B):
                        # Thêm 2 nhóm này vào mảng có cặp
                        add_khong_trung(arr_co_cap, nhom_A, nhom_B)
                        check = True
                        dem += 1
                        
                        chi_so = nhom_A.p_chi_so + nhom_B.p_chi_so
                        ma_nhom_a = nhom_A.p_ma_nhi_phan 
                        ma_nhom_b = nhom_B.p_ma_nhi_phan
                        maNP = ma_nhi_phan_moi(ma_nhom_a, ma_nhom_b)

                        nhom_new = PhanTu(self.so_bien, chi_so)
                        nhom_new.p_ma_nhi_phan = maNP
                        add_khong_trung(arr_new, nhom_new)

                if dem==0 and(not check_ton_tai(arr_co_cap, nhom_A)):
                    add_khong_trung(arr_pi, nhom_A)
            if not check_ton_tai(arr_co_cap, arr_all[size - 1]):
                add_khong_trung(arr_pi, arr_all[size - 1])
            if not check: 
                for x in arr_all: add_khong_trung(arr_pi, x)
                break
            arr_all = arr_new.copy()
            arr_new = []
            arr_co_cap = [] 
        return arr_pi

    # Hàm trả về các Essential 
    def arr_essential(self):
        arr_pi = self.arr_prime_implicant()
        arr_mintern = self.mintern.copy()
        arr_mintern.sort()

        size = len(arr_mintern)
        arr_chi_so = [x.p_chi_so for x in arr_pi]

        # arr_count là mảng đối chiếu với mintern 
        arr_count = [0]*size 
        for i in range(size):
            for arr_num in arr_chi_so:
                for j in range(len(arr_num)):
                    if arr_num[j] == arr_mintern[i]: 
                        arr_count[i] += 1 
                    else: 
                        arr_count[i] += 0
        
        arr_ess = []
        for i in range(size):
            count = arr_count[i] 
            value = arr_mintern[i]
            if count == 1:
                for item in arr_pi:
                    if item.p_chi_so.count(value) > 0: 
                        add_khong_trung(arr_ess, item)
        return arr_ess

    
    # Hàm trả về các cặp nonEssential (tổ hợp nhỏ nhất)
    def arr_non_essential(self):
        cot_con_trong = self.mintern.copy()
        arr_ess = self.arr_essential()
        arr_pi = self.arr_prime_implicant() 

        for item in arr_ess:
            for num in item.p_chi_so:
                if cot_con_trong.count(num) > 0:
                    cot_con_trong.remove(num)
        # Nếu không còn cột nào trống thì trả về mảng rỗng
        if len(cot_con_trong) == 0: return []
        
        # Lấy mảng để tổ hợp 
        arr_temp = []
        con_lai = [x for x in arr_pi if x not in arr_ess]
        for num in cot_con_trong:
            arr_row = []
            for item in con_lai:
                if item.p_chi_so.count(num) > 0:
                    add_khong_trung(arr_row, item)
            arr_temp.append(arr_row)
        return to_hop_nhom(arr_temp)

class Result:
    # Với arr_input là các mảng truyền vào dạng các mintern or maxtern
    # type: loại input truyền vào 
    # type = 1 thì input là mintern
    # type = 2 thì input là maxtern
    def __init__(self,so_bien, arr_input, arr_dont_care, type):
        self.arr_dont_care = arr_dont_care.copy()
        self.so_bien = so_bien
        self.type = type
        if type == 1:
            self.arr_maxtern = [x for x in range(2**so_bien)
            if x not in arr_input and x not in arr_dont_care]
            self.arr_mintern = arr_input.copy()
        elif type == 2:
            self.arr_mintern = [x for x in range(2**so_bien) 
            if x not in arr_input and x not in arr_dont_care]
            self.arr_maxtern = arr_input.copy()
        
    # Lấy f(A,B,C,D,....) = 
    def __function(self):
        arr = [chr(ord('A')+i) for i in range(self.so_bien)]
        fStr = "f(" 
        for i in range(len(arr) - 1):
            fStr += arr[i] + ","
        return fStr + arr[len(arr) - 1] + ") = "

    # Hàm trả về mảng các kết quả dạng SOP(tổng các tích) mintern
    def sop_result(self):
        xl = XuLy(self.so_bien, self.arr_mintern, self.arr_dont_care)
        arr_ess = xl.arr_essential()
        arr_non_ess = xl.arr_non_essential()

        str_temp = self.__function()
        for item in arr_ess:
            str_temp += item.code_mintern + " + "
        if len(arr_non_ess) == 0: return [str_temp[:len(str_temp)-3]]
        
        arr_result = []
        for item in arr_non_ess:
            str_  = str_temp 
            for x in item: str_ += x.code_mintern + " + "
            arr_result.append(str_[:len(str_)-3])
        return arr_result

    # Hàm trả về mảng các kết quả dạng POS(tích các tổng) maxtern
    def pos_result(self):
        xl = XuLy(self.so_bien, self.arr_maxtern, self.arr_dont_care)
        arr_ess = xl.arr_essential()
        arr_non_ess = xl.arr_non_essential()

        str_temp = self.__function()
        for item in arr_ess:
            str_temp += item.code_maxtern
        if len(arr_non_ess) == 0: return [str_temp]
        
        arr_result = []
        for item in arr_non_ess:
            str_  = str_temp 
            for x in item: str_ += x.code_maxtern
            arr_result.append(str_)
        return arr_result

# File Main 

arr_input = [2, 4, 5, 6, 10, 0, 9]
arr_dont_care = [7, 11, 12, 13, 14, 15]
so_bien = 4

# type = 1: arr_input là mintern 
# type = 2: arr_input là maxtern 
kq = Result(so_bien, arr_input, arr_dont_care, type=1)
print('Kết quả dạng tổng các tích: ')
for i in kq.sop_result():
    print(i)

print('Kết quả dạng tích các tổng: ')
for i in kq.pos_result():
    print(i)
