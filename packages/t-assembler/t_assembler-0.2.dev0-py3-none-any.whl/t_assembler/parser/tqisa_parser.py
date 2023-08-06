
# A general structure of binary format:
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | Q ||        Opcode         ||        rd        ||        rs        ||        rt        ||             X             
#    ------------------------------------------------------------------------------------------------------------------------
#
#
# ADD：opcode = 30 
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   1   1   1   1   0 ||        rd        ||        rs        ||        rt        ||             X             
#    ------------------------------------------------------------------------------------------------------------------------
#
#
# SUB：opcode = 31
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   1   1   1   1   1 ||        rd        ||        rs        ||        rt        ||             X            
#    ------------------------------------------------------------------------------------------------------------------------ 
#
#
#
# MOV：opcode = 22
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   1   0   1   1   0 ||        rd        ||                               imm             
#    ------------------------------------------------------------------------------------------------------------------------ 
#
#
# MVN：opcode = 23
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   1   0   1   1   1 ||        rd        ||                               imm             
#    ------------------------------------------------------------------------------------------------------------------------ 
#
#
# CMP：opcode = 13
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   0   1   1   0   1 ||        X         ||        rs        ||        rt        ||             X            
#    ------------------------------------------------------------------------------------------------------------------------ 
#
#
# GOTO：opcode = 2
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   0   0   0   1   0 ||                                     addr             
#    ------------------------------------------------------------------------------------------------------------------------
#
# B   : opcode = 3(EQ), 4(NE), 5(GT), 6(LT)
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   0   0   0   1   1 ||                                     addr                                        
#    ------------------------------------------------------------------------------------------------------------------------
#
# MRCEP: opcode = 8
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   0   1   0   0   0 ||                                addr                                 ||       qd    
#    ------------------------------------------------------------------------------------------------------------------------
#
# MRCEN: opcode = 9
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 0   0   1   1   0   0 ||                                addr                                 ||       qd    
#    ------------------------------------------------------------------------------------------------------------------------
#
# SMIS: opcode = 32
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 1   0   0   0   0   0 ||         sd           ||   pos   ||                     s_mask
#    ------------------------------------------------------------------------------------------------------------------------
#
#
# SMIT: opcode = 40
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 1   0   1   0   0   0 ||         td           ||   pos   ||                     t_mask
#    ------------------------------------------------------------------------------------------------------------------------
#
#
# QWAIT:opcode = 48
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 0 || 1   1   0   0   0   0 ||        X        ||                            imm
#    ------------------------------------------------------------------------------------------------------------------------
#

# Quantum operation instruction
#
#    --31--30--29--28--27--26--25--24--23--22--21--20--19--18--17--16--15--14--13--12--11--10--9--8--7--6--5--4--3--2--1--0--
#    ------------------------------------------------------------------------------------------------------------------------
#    | 1 ||                        X                             ||          q_op_opcode        ||  mask_reg_addr ||pre_interval
#    ------------------------------------------------------------------------------------------------------------------------
#


import json



#Tell if a string starts with an integer number
def starts_with_int(string):
    i = 0
    while i < len(string):
        if not string[i].isdigit():
            break
        else:
            i += 1

    if i == 0:
        return False, 0
    else:
        #when string length >=1 and it starts with an integer number
        return True, i

#Remove the integer number at the beginning of string
def rm_int(string):
    if len(string) > 1:
        i = 0
        while string[i].isdigit():
            i += 1
            if i >= len(string):
                break
            elif not string[i].isdigit():
                break
            else:
                pass
        return string[i:]
    else:
        return ""

#find the nth occurence of character
def find_nth(string, character, n):
    start = string.find(character)
    while start >= 0 and n > 1:
        start = string.find(character, start+len(character))
        n -= 1
    return start


class AsmParser(object):
    def __init__(self):
        """Constructor"""
        self.rd_success = True
        self.len_line = 0
        self.error = ""
        self.error_start = 0
        self.error_message = ""
        self.insn_names = ["smis", "smit", "add", "sub", "mov", "mvn", "cmp", "beq", "bne", "blt", "bgt", "goto", "qwait", 'mrcep', 'mrcen']
        self.opcode = {
            "smis":     32,
            "smit":     40, 
            "cmp":      13,
            "goto":     2,
            'beq':      3,
            'bne':      4,
            'bgt':      5,
            'blt':      6, 
            "add":      30, 
            "sub":      31, 
            "mov":      22, 
            "mvn":      23, 
            "mrcep":    8, 
            "mrcep":    9, 
            "qwait":    48,  
        }
        self.flag_address = {}
        self.flag_with_insn = {}
        self.num_qubits = 0
        self.num_edges = 0
        self.edge_address = []

        self.single_qubit_opcode = {}
        self.single_qop_name = []
        self.two_qubit_opcode = {}
        self.two_qop_name = []
        self.qop_name = []

        self.dec_insn = 0
        self.dec_insn_list = []

        self.num_t_reg = 64
        self.num_s_reg = 64
        self.num_r_reg = 32


    def check_digit(self, target):
        pass

    def check_comma(self, target):
        pass
 
    def gen_error(self, error, parent, type, value, pos_add):
        self.error = error
        if parent != None:
            pos = parent.find(error)
        else:
            pos = 0
        self.error_start = self.num_ele_before + pos + pos_add
        if type == "syntax":
            if value == "digit":
                self.error_message = "syntax error, unexpected '" + self.error + "', expecting an integer number at here"
            elif value == "COMMA":
                self.error_message = "syntax error, unexpected '" + self.error + "', expecting COMMA at here"
            else:
                self.error_message = "syntax error, unexpected '" + self.error + "', expecting " + value + " at here"
        else:
            self.error_message = "error occured"



    def check_digit_comma(self, target):
        self.num_ele_before += self.true_line.find(self.elements) + self.elements.find(target)

        #digit, digit, digit
        if len(target) == 0:
            self.gen_error(target, target, "syntax", "digit", 0)
            return False
        #length = 1
        elif len(target) == 1:
            if target.isdigit():
                return True
            else:
                self.gen_error(target, target, "syntax", "digit", 0)
                return False
        #length > 1
        else:
            if not target[0].isdigit():
                self.gen_error(target[0], target, "syntax", "digit", 0)
                return False
            else:
                prev_value = "digit"
                target_itr = target
                for i in range(0, len(target) - 2):
                    #after a digit, a comma is required (after stripping)
                    if target_itr[0].isdigit():
                        prev_value = "digit"
                        if (target_itr[1:].strip()[0] is not ",") and (not target_itr[1:].strip()[0].isdigit()):
                            self.gen_error(target_itr[1:].strip()[0], target_itr[1:], "syntax", "COMMA", i + 1)
                            return False
                    #after a comma, a digit is required (after stripping)
                    elif target_itr[0] is ",":
                        prev_value = "comma"
                        if not target_itr[1:].strip()[0].isdigit():
                            self.gen_error(target_itr[1:].strip()[0], target_itr[1:], "syntax", "digit", i + 1)
                            return False
                    #if current digit is other symbols
                    elif target_itr[0] is not " ": 
                        if prev_value is "digit":
                            expect_name = "COMMA"
                        else:
                            expect_name = "digit"
                        self.gen_error(target_itr[1:].strip()[0], target_itr[1:], "syntax", expect_name, i + 1)

                        return False
                    else:
                        pass

                    target_itr = target_itr[1:]

                #if the last digit is not an integer
                if not target[len(target) - 1].isdigit():
                    self.gen_error(target[len(target) - 1], None, "syntax", "digit", len(target) - 1)
                    return False
            return True



    def is_qubit_pair(self, target):
        #qubit pair: (1, 2) ...
        if not target.startswith('('):
            self.gen_error(target[0], target, 'syntax', 'PAREN open', 0)
            return False, 0
        else:
            if not starts_with_int(target[1:])[0]:
                pos = starts_with_int(target[1:])[1]
                self.gen_error(target[1:][pos], target[1:], 'syntax', 'digit', 1)
                return False, 0
            else:    
                target_rmd1 = rm_int(target[1:])
                self.num_ele_before += target.find(target_rmd1)

                for i in range(0, len(target_rmd1) - 2):
                    if (not target_rmd1[i].isdigit()) and (target_rmd1[i:].strip()[0] is not ","):
                        self.gen_error(target_rmd1[i:].strip()[0], target_rmd1[i:], 'syntax', 'COMMA', i)
                        return False, 0
                    elif target_rmd1[i:].strip()[0] is ',':
                        target_itr = target_rmd1[i:].strip()[1:].strip()
                        break
                    else:
                        target_itr = target_rmd1[i:]

                self.num_ele_before += target_rmd1.find(target_itr)
                if not starts_with_int(target_itr)[0]:
                    pos = starts_with_int(target_itr)[1]
                    self.gen_error(target_itr[pos], target_itr, 'syntax', 'digit', 0)
                    return False, 0
                else:
                    target_rmd2 = rm_int(target_itr)
                    if not target_rmd2.strip().startswith(')'):
                        self.gen_error(target_rmd2.strip()[0], target_rmd2, 'syntax', 'PAREN close', target_itr.find(target_rmd2))
                        return False, 0
                    else:
                        return True, target.find(')')



    def check_pair_comma(self, target):
        self.num_ele_before += self.true_line.find(self.elements) + self.elements.find(target)

        #(0, 2), (6, 4)
        if len(target) == 0:
            self.gen_error('', target, 'syntax', 'a qubit pair', 0)
            return False
        else:
            while True:
                if len(target) < 5:
                    self.gen_error(target, target, 'syntax', 'a qubit address', 0)
                    return False
                else:
                    is_pair, pair_width = self.is_qubit_pair(target)
                    if is_pair:
                        target = target[(pair_width + 1):].strip()
                        if len(target) == 0:
                            return True
                        elif not target.startswith(','):
                            print("aaa")
                            self.gen_error(target[0], target, 'syntax', 'COMMA', 0)
                            return False
                        else:
                            target = target[1:].strip()
                    else:
                        #do not need to generate error information again
                        return False

    def check_reg_int(self, target, s_t_r_q):
        elements_itr = target

        if not elements_itr.startswith(s_t_r_q):
            self.gen_error(elements_itr[0], elements_itr, "syntax", "register type " + s_t_r_q.upper(), 0)
            return False, None
        else:
            elements_itr = elements_itr[1:]
            self.num_ele_before += 1
            if not starts_with_int(elements_itr)[0]:
                pos = starts_with_int(elements_itr)[1]
                self.gen_error(elements_itr[pos], elements_itr, 'syntax', 'digit', 0)
                return False, None
            else:
                elements_itr_new = rm_int(elements_itr).strip()    
                self.num_ele_before += elements_itr.find(elements_itr_new)

                return True, elements_itr_new

    def check_reg_int_comma(self, target, s_or_t_or_r):

        check_success, elements_itr = self.check_reg_int(target, s_or_t_or_r)
        if not check_success:
            return False, None
        else:
            if not elements_itr.startswith(','):
                self.gen_error(elements_itr[0], elements_itr, 'syntax', 'COMMA', 0)
                return False, None
            else:
                self.num_ele_before += elements_itr.find(elements_itr[1:].strip())
                elements_itr = elements_itr[1:].strip()
                return True, elements_itr



    def check_SMI(self, s_or_t):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: sd, {1, 2, 3}/td, {(0, 2), (6, 4)}     

        if not self.check_reg_int_comma(self.elements, s_or_t)[0]:
            return False
        else:
            #{1, 2, 3}/{(0, 2), (6, 4)}
            elements_itr = self.check_reg_int_comma(self.elements, s_or_t)[1]

            if not elements_itr.startswith("{"):
                self.gen_error(elements_itr[0], elements_itr, "syntax", "BRACE open", 0)
                return False
            elif not elements_itr.endswith("}"):
                self.gen_error(elements_itr[len(elements_itr) - 1], elements_itr, "syntax", "BRACE close", 0)
                return False
            else:
                elements_itr = elements_itr[1:(len(elements_itr) - 1)].strip()
                if s_or_t is "s":
                    return self.check_digit_comma(elements_itr.strip())
                else: 
                    return self.check_pair_comma(elements_itr.strip())
            


    def generate_bin_SMIS(self):
        #syntax: sd, {1, 2, 3}
        s_reg_num = int(self.elements.split(',')[0].split('s')[1])
        s_mask = self.elements.split('{')[1].split('}')[0] 
        s_mask_list = s_mask.split(',')
        s_mask_list = list(map(int, s_mask_list))

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += s_reg_num << 19
        for entry in s_mask_list:
            self.dec_insn += 1 << entry
        self.dec_insn_list.append(self.dec_insn)

        return True
        

    
    def generate_bin_SMIT(self):
        #syntax: sd, {(1, 2) , (6, 4)}
        pair_list = []
        qubit_pair_list = []
        edge_list = []
        t_mask_list = []

        t_reg_num = int(self.elements.split(',')[0].split('t')[1])
        #check if register index exceeds the number of T register
        if t_reg_num >= self.num_t_reg:
            self.error = self.elements[(self.elements.find('t') + 1) : (self.elements.find(str(t_reg_num)) + len(str(t_reg_num)))]
            self.error_start = self.true_line.find(self.error)
            self.error_message = "T register number " + str(t_reg_num) + " exceeds."
            return False

        t_mask = self.elements.split('{')[1].split('}')[0] 
        while True:
            pair_start = t_mask.find('(')
            pair_end = t_mask.find(')')
            if (pair_start == -1 or pair_end == -1): 
                break
            else:
                pair_list.append(t_mask[(pair_start + 1):pair_end])
                t_mask = t_mask[(pair_end + 1):]

        #decode all edges from insn
        for i in range(0, len(pair_list)):
            pair = pair_list[i].strip('(').strip(')')
            qubit_left, qubit_right = pair.split(',')[0], pair.split(',')[1]
            qubit_pair_list.append((int(qubit_left), int(qubit_right)))

        #find the edge index
        for i in range(0, len(qubit_pair_list)):
            find_edge = False
            for j in range(0, self.num_edges):
                if (qubit_pair_list[i][0] == self.edge_address[j]["src"]) and \
                (qubit_pair_list[i][1] == self.edge_address[j]["dst"]):
                    t_mask_list.append(self.edge_address[j]["id"])
                    find_edge = True

            if not find_edge:
                print(find_nth(self.true_line, '(', i + 1))
                self.error = self.true_line[find_nth(self.true_line, '(', i + 1):(find_nth(self.true_line, ')', i + 1) + 1)]
                self.error_start = self.true_line.find(self.error)
                self.error_message = "Edge address corresponding to qubit pair '" + str(qubit_pair_list[i]) \
                + "' is not found."
                return False
        
        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += t_reg_num << 19
        for entry in t_mask_list:
            self.dec_insn += 1 << entry
        self.dec_insn_list.append(self.dec_insn)

        return True



    def generate_SMI(self):
        #syntax: SMIS  sd, {1, 2, 3}
        if self.insn_name == "smis":
            if self.check_SMI("s"):
                if self.generate_bin_SMIS():
                    return True
                else:
                    return False
            else:
                return False

        #syntax: SMIT  td, {(0, 2), (6, 4)}
        else:
            if self.check_SMI("t"):
                if self.generate_bin_SMIT():
                    return True
                else:
                    return False
            else:
                return False



    def check_CMP(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: rs, rt
        elements_itr = self.elements

        check_success, elements_itr = self.check_reg_int_comma(elements_itr, 'r')
        if not check_success:
            return False
        else:
            check_success, elements_itr = self.check_reg_int(elements_itr, 'r')
            if not check_success:
                return False
            else:
                if " " in elements_itr:
                    self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                        'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
                    return False
                else:
                    return True


    def generate_bin_CMP(self): 
        reg_list = list(reg.strip() for reg in self.elements.split(','))
        reg_list = list(int(reg.split('r')[1]) for reg in reg_list)

        for i in range(0, len(reg_list)):
            if reg_list[i] >= self.num_r_reg:
                self.error = self.true_line[find_nth(self.true_line, 'r',i + 1):find_nth(self.true_line, ',', i + 1)].strip()
                self.error_start = self.true_line.find(self.error)
                self.error_message = "R register number " + str(reg_list[i]) + " exceeds"
                return False

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += reg_list[0] << 15
        self.dec_insn += reg_list[1] << 10
        self.dec_insn_list.append(self.dec_insn)

        return True

    def generate_CMP(self):
        if self.check_CMP():
            if self.generate_bin_CMP():
                return True
            else:
                return False
        else:
            return False


    def check_B(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: flag_symbol
        elements_itr = self.elements
        
        if " " in elements_itr:
            self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
            return False
        else:
            return True

    def generate_bin_B(self):
        flag_symbol = self.elements.strip()

        if flag_symbol not in self.flag_address:
                self.error = flag_symbol
                self.error_start = self.num_ele_before
                self.error_message = "branch address for '" + str(self.error) + "' is not found."
                return False
        else: 
            address = self.flag_address[flag_symbol]

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += address 
        self.dec_insn_list.append(self.dec_insn) 

        return True

    def generate_B(self):
        if self.check_B():
            if self.generate_bin_B():
                return True
            else:
                return False
        else:
            return False



    def check_GOTO(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: flag_symbol
        elements_itr = self.elements
        
        if " " in elements_itr:
            self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
            return False
        else:
            return True

    def generate_bin_GOTO(self):
        flag_symbol = self.elements.strip()

        if flag_symbol not in self.flag_address:
                self.error = flag_symbol
                self.error_start = self.num_ele_before
                self.error_message = "branch address for '" + str(self.error) + "' is not found."
                return False
        else: 
            address = self.flag_address[flag_symbol]

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += address 
        self.dec_insn_list.append(self.dec_insn) 

        return True

    def generate_GOTO(self):
        if self.check_GOTO():
            if self.generate_bin_GOTO():
                return True
            else:
                return False
        else:
            return False



    def check_MRCE(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: qd, flag_address
        elements_itr = self.elements

        check_success, elements_itr = self.check_reg_int_comma(elements_itr, 'q')
        if not check_success:
            return False
        else:
            if " " in elements_itr:
                self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                    'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
                return False
            else:
                return True


    def generate_bin_MRCE(self):
        reg_num = int(self.elements.split(',')[0].split('q')[1])
        flag_symbol = self.elements.split(',')[1].strip()

        if flag_symbol not in self.flag_address:
                self.error = flag_symbol
                self.error_start = self.num_ele_before
                self.error_message = "branch address for '" + str(self.error) + "' is not found."
                return False
        else: 
            address = self.flag_address[flag_symbol]

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += address << 6
        self.dec_insn += reg_num 
        self.dec_insn_list.append(self.dec_insn) 

        return True

    def generate_MRCE(self):
        if self.check_MRCE():
            if self.generate_bin_MRCE():
                return True
            else:
                return False
        else:
            return False



    def check_arithmetic(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: rd, rs, rt
        elements_itr = self.elements

        for i in range(0, 2):
            check_success, elements_itr = self.check_reg_int_comma(elements_itr, 'r')
            if not check_success:
                return False
            else:
                pass

        check_success, elements_itr = self.check_reg_int(elements_itr, 'r')
        if not check_success:
                return False
        else:
            if len(elements_itr.strip()) > 0:
                self.gen_error(elements_itr.strip()[0], elements_itr, 'syntax', 'NEWLINE', 0)
                return False

        return True



    def generate_bin_arithmetic(self):
        reg_list = list(reg.strip() for reg in self.elements.split(','))
        reg_list = list(int(reg.split('r')[1]) for reg in reg_list)

        for i in range(0, len(reg_list)):
            if reg_list[i] >= self.num_r_reg:
                self.error = self.true_line[find_nth(self.true_line, 'r',i + 1):find_nth(self.true_line, ',', i + 1)].strip()
                self.error_start = self.true_line.find(self.error)
                self.error_message = "R register number " + str(reg_list[i]) + " exceeds"
                return False

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += reg_list[0] << 20
        self.dec_insn += reg_list[1] << 15
        self.dec_insn += reg_list[2] << 10
        self.dec_insn_list.append(self.dec_insn)

        return True

    def generate_arithmetic(self):
        if self.check_arithmetic():
            if self.generate_bin_arithmetic():
                return True
            else:
                return False
        else:
            return False



    def check_MV(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: rd, imm
        elements_itr = self.elements

        check_success, elements_itr = self.check_reg_int_comma(elements_itr, 'r')
        if not check_success:
            return False
        else:
            #only an immediate number left
            if not starts_with_int(elements_itr)[0]:
                pos = starts_with_int(elements_itr)[1]
                self.gen_error(elements_itr[pos], elements_itr, 'syntax', 'digit', 0)
                return False
            else:
                elements_itr_new = rm_int(elements_itr).strip()
                self.num_ele_before += elements_itr.find(elements_itr_new)
                if len(elements_itr_new) > 0:
                    self.gen_error(elements_itr_new[0], elements_itr_new, 'syntax', 'NEWLINE', 0)
                    return False
            
        return True


    def generate_bin_MV(self):
        reg_num = int(self.elements.split(',')[0].split('r')[1].strip())
        if reg_num >= self.num_r_reg:
            self.error = self.true_line[find_nth(self.true_line, 'r', 1):find_nth(self.true_line, ',', 1)].strip()
            self.error_start = self.true_line.find(self.error)
            self.error_message = "R register number " + str(reg_list[i]) + " exceeds"
            return False
        imm_value = int(self.elements.split(',')[1].strip())

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += imm_value 
        self.dec_insn_list.append(self.dec_insn)

        return True
            

    def generate_MV(self):
        if self.check_MV():
            if self.generate_bin_MV():
                return True
            else:
                return False
        else:
            return False



    def check_QWAIT(self):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: imm
        elements_itr = self.elements
        if not starts_with_int(elements_itr)[0]:
            pos = starts_with_int(elements_itr)[1]
            self.gen_error(elements_itr[pos], elements_itr, 'syntax', 'digit', 0)
            return False
        else:
            elements_itr_new = rm_int(elements_itr).strip()
            self.num_ele_before += elements_itr.find(elements_itr_new)
            if len(elements_itr_new) > 0:
                self.gen_error(elements_itr_new[0], elements_itr_new, 'syntax', 'NEWLINE', 0)
                return False
        
        return True

    def generate_bin_QWAIT(self):      
        imm_value = int(self.elements)

        self.dec_insn = 0
        self.dec_insn += (self.opcode[self.insn_name]) << 25 
        self.dec_insn += imm_value 
        self.dec_insn_list.append(self.dec_insn)

        return True

    def generate_QWAIT(self):
        if self.check_QWAIT():
            if self.generate_bin_QWAIT():
                return True
            else:
                return False
        else:
            return False



    def check_pure_qop_insn(self, s_or_t):
        self.num_ele_before += self.true_line.find(self.elements)
        #check syntax error
        #syntax: sd/td
        elements_itr = self.elements

        check_success, elements_itr = self.check_reg_int(elements_itr, s_or_t)
        if not check_success:
            return False
        else:
            if " " in elements_itr:
                self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                    'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
                return False
            else:
                return True


    def generate_bin_pure_qop_insn(self, s_or_t):
        #if the pre_interval is not being specified, a default wait time 1 is used    
        reg_num = int(self.elements.split(s_or_t)[1].strip())
        if reg_num >= self.num_s_reg:
            self.error = self.true_line[find_nth(self.true_line, s_or_t, 1):find_nth(self.true_line, ',', 1)].strip()
            self.error_start = self.true_line.find(self.error)
            self.error_message = s_or_t.upper() + " register number " + str(reg_list[i]) + " exceeds"
            return False
        imm_value = 1

        self.dec_insn = 0
        if s_or_t is 's':
            self.dec_insn += (self.single_qubit_opcode[self.insn_name]) << 9
        elif s_or_t is 't':
            self.dec_insn += (self.two_qubit_opcode[self.insn_name]) << 9

        self.dec_insn += (reg_num << 3)
        self.dec_insn += imm_value 
        self.dec_insn += 1 << 31
        self.dec_insn_list.append(self.dec_insn)

        return True

    def generate_pure_qop_insn(self, s_or_t):
        if self.check_pure_qop_insn(s_or_t):
            if self.generate_bin_pure_qop_insn(s_or_t):
                return True
            else:
                return False
        else:
            return False



    def check_qop_insn(self):
        #self.true_line: bs 0 q_opcode sd/td
        elements_itr = self.true_line.split('bs')[1].strip()

        if not starts_with_int(elements_itr)[0]:
            pos = starts_with_int(elements_itr)[1]
            self.gen_error(elements_itr[pos], elements_itr, 'syntax', 'digit', 0)
            return False, None
        else:
            elements_itr_new = rm_int(elements_itr).strip()    
            self.num_ele_before += elements_itr.find(elements_itr_new)
            q_opcode = elements_itr_new.split()[0].strip()
            if q_opcode in self.single_qop_name:
                elements_itr = elements_itr_new.split()[1].strip()
                self.num_ele_before += elements_itr_new.find(elements_itr)

                check_success, elements_itr = self.check_reg_int(elements_itr, 's')
                if not check_success:
                    return False, None
                else:
                    if " " in elements_itr:
                        self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                            'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
                        return False, None
                    else:
                        return True, 's'
            elif q_opcode in self.two_qop_name:
                elements_itr = elements_itr_new.split()[1].strip()
                self.num_ele_before += elements_itr_new.find(elements_itr)

                check_success, elements_itr = self.check_reg_int(elements_itr, 't')
                if not check_success:
                    return False, None
                else:
                    if " " in elements_itr:
                        self.gen_error(elements_itr.rsplit(' ', 1)[1].strip(), elements_itr.rsplit(' ', 1)[1], \
                            'syntax', 'NEWLINE', len(elements_itr.rsplit(' ', 1)[0]) + 1)
                        return False, None
                    else:
                        return True, 't'
            else:
                self.error = q_opcode
                self.error_start = elements_itr_new.find(q_opcode) + self.num_ele_before
                self.error_message = "opcode for '" + str(self.error) + "' is not found."
                return False, None



    def generate_bin_qop_insn(self, s_or_t):
        elements_itr = self.true_line.split('bs')[1].strip()
        imm_value = int(elements_itr.split()[0].strip())
        q_opcode = elements_itr.split()[1].strip()
        reg = elements_itr.split()[2].strip()
        reg_num = int(reg.split(s_or_t)[1])

        self.dec_insn = 0
        if s_or_t is 's':
            self.dec_insn += (self.single_qubit_opcode[q_opcode]) << 9 
        elif s_or_t is 't':
            self.dec_insn += (self.two_qubit_opcode[q_opcode]) << 9

        self.dec_insn += (reg_num << 3)
        self.dec_insn += imm_value 
        self.dec_insn += 1 << 31
        self.dec_insn_list.append(self.dec_insn)
        
        return True

    def generate_qop_insn(self):
        success, s_or_t = self.check_qop_insn()
        if success:
            if self.generate_bin_qop_insn(s_or_t):
                return True
            else:
                return False
        else:
            return False



    def parse(self, line):
        #index of instructions (neglect blank line, flag lines, comment lines...)
        self.true_line_index += 1

        line_elements = []
        insn_name_switcher = {
            "smis":     "generate_SMI",
            "smit":     "generate_SMI", 
            "cmp":      "generate_CMP",
            "goto":     "generate_GOTO", 
            "beq":      "generate_B",
            "bne":      "generate_B",
            "blt":      "generate_B",
            "bgt":      "generate_B",
            "add":      "generate_arithmetic", 
            "sub":      "generate_arithmetic", 
            "mov":      "generate_MV", 
            "mvn":      "generate_MV", 
            "mrcep":    "generate_MRCE", 
            "mrcen":    "generate_MRCE", 
            "qwait":    "generate_QWAIT",  
        }

        #Line wih useful information for instruction
        self.true_line = line.strip()
        self.num_ele_before += line.find(self.true_line)
        line_elements = self.true_line.partition(" ")
        #if this is a quantum instruction with bs
        if line_elements[0].strip() == 'bs':
            genb_success = self.generate_qop_insn()
            return genb_success
        #elelments: instruction content without instruction name
        self.elements = line_elements[2].strip()
        self.insn_name = line_elements[0].strip()

        if self.insn_name in self.insn_names:
            # insn_name_switcher[insn_name].__call__()
            genb_success = getattr(self, insn_name_switcher[self.insn_name])()
            return genb_success
        elif self.insn_name in self.single_qop_name:
            genb_success = self.generate_pure_qop_insn('s')
            return genb_success
        elif self.insn_name in self.two_qop_name:
            genb_success = self.generate_pure_qop_insn('t')
            return genb_success
        else:
            self.error = self.insn_name
            self.error_start = self.true_line.find(self.insn_name) + self.num_ele_before
            self.error_message = "opcode for '" + str(self.error) + "' is not found."
            return False


    def decode_flag(self):
        #flag_address: (empty or insn)

        #store the flag address
        flag = self.line.split(':')[0].strip()
        self.line_part = self.line.split(':')[1].strip()
        if " " in flag:
            self.gen_error(flag, self.line, syntax, 'flag address', 0)
            return False
        else:
            self.flag_address[flag] = self.true_line_index

        return True


    def read_file(self, in_file_name):
        with open(in_file_name, 'r') as rf:
            self.line_index = 0
            self.true_line_index = 0

            lines = (line.rstrip() for line in rf)
            lines = list(line for line in lines)

            #store all flag address at first
            for self.line in lines:
                self.line = self.line.lower()
                if self.line:
                    if ":" in self.line:
                        self.rd_success = self.decode_flag()
                        if not self.rd_success:
                            break
            print(self.flag_address)
            #do real parse
            for self.line in lines:
                self.line = self.line.rstrip().lower()
                self.line_index += 1
                self.len_line = len(self.line)
                self.num_ele_before = 0

                #neglect blank lines
                if self.line:
                    #Remove the comment in line, do nothing if this line only has comment
                    if "#" in self.line:
                        self.line_part = self.line.strip().split("#")[0]
                        if self.line_part == "":
                            pass
                        else:
                            self.rd_success = self.parse(self.line_part)
                            if not self.rd_success:
                                break

                    #This line contains a flag address
                    elif ":" in self.line:
                        self.rd_success = self.decode_flag()
                        #continue to parse the line if there is insn remains
                        if len(self.line_part) > 0:
                            self.num_ele_before += self.line.find(':')
                            self.num_ele_before += self.line.split(':')[1].find(self.line_part)
                            self.num_ele_before += 1
                            self.rd_success = self.parse(self.line_part)  

                    #Parse the instruction
                    else:
                        self.rd_success = self.parse(self.line)
                        if not self.rd_success:
                            break

            print(self.flag_address)

        rf.close()


    def read_hardware_config(self, in_fn):
        with open(in_fn) as rf:
            hardware_config = json.load(rf)

        self.num_qubits = hardware_config["topology"]["num_qubits"]
        self.num_edges = hardware_config["topology"]["edges"]["count"]
        for i in range(0, self.num_edges):
            self.edge_address.append(hardware_config["topology"]["edges"]["address"][i])


    def read_qopcode_config(self, in_fn):
        with open(in_fn) as rf:
            qopcode_config = json.load(rf)

        #need to be case insensitive
        for entry in qopcode_config["single_qubit_opcode"]:
            self.single_qubit_opcode[entry.lower()] = qopcode_config["single_qubit_opcode"][entry]
            self.single_qop_name.append(entry.lower()) 
        for entry in qopcode_config["two_qubit_opcode"]:
            self.two_qubit_opcode[entry.lower()] = qopcode_config["two_qubit_opcode"][entry]
            self.two_qop_name.append(entry.lower())

        self.qop_name = [self.single_qop_name, self.two_qop_name]


    def write_file(self, out_file_name):
        with open(out_file_name, 'wb') as file:
            for i in range(0, len(self.dec_insn_list)):
                file.write((self.dec_insn_list[i]).to_bytes(4, byteorder='little', signed=False))


    def print_hex_insns(self):
        print("Generated instructions:")
        for insn in self.dec_insn_list:
            print("\t" + "0x" + format(insn, '08x'))


    def report_error(self):
        line_prefix = str(self.line_index) + ": "
        error_line =  line_prefix + self.line.lower() 
        if len(self.error) > 0:
            marker_line = " " * (self.error_start + len(line_prefix)) + "^" * len(self.error)
        else:
            marker_line = " " * self.error_start + "^"

        print("-" * 50)
        print(error_line)
        print(marker_line)
        print("-" * 50)
        print("\n" + self.error_message)

