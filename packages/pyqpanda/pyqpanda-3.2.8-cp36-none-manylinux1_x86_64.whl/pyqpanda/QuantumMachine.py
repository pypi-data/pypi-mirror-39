import pyqpanda as pywrap

class QuantumMachine:
    def __init__(self, backend_type = pywrap.QuantumMachine_type.CPU_SINGLE_THREAD):
        self._quantum_machine = pywrap.init_quantum_machine(backend_type)

    def init(self):
        pass

    def qAlloc(self):
        return self._quantum_machine.qAlloc()

    def cAlloc(self):
        return self._quantum_machine.cAlloc()

    def qFree(self, qubit):
        return self._quantum_machine.qFree(qubit)

    def cFree(self, cbit):
        return self._quantum_machine.cFree(cbit)

    def load(self, qprog):
        self._quantum_machine.load(qprog)

    def append(self, qprog):
        self._quantum_machine.append(qprog)

    def run(self):
        self._quantum_machine.run()

    def getResult(self):
        return self._quantum_machine.getResult()

    def getResultMap(self):
        result = self.getResult()
        result_map = result.getResultMap()
        return result_map
        
    def finalize(self):
        self._quantum_machine.finalize()

    def getCBitValue(self, cbit):
        resultMap = self.getResultMap()
        cbit_name = cbit.getName()
        return resultMap[cbit_name]
    
    def qAlloc_many(self, alloc_num):
        """
        `Extended QPanda API` \n
        Allocate a list of qubit \n
        int -> list<Qubit>  
        """
        qubit_list=list()
        for q in range(0,alloc_num):
            qubit_list.append(self.qAlloc())
        return qubit_list    

    def cAlloc_many(self, alloc_num):
        """
        `Extended QPanda API` \n
        Allocate a list of cbit \n
        int -> list<CBit>  
        """
        cbit_list=list()
        for i in range(0,alloc_num):
            cbit_list.append(self.cAlloc())
        return cbit_list
        
    def qFree_all(self, qubit_list):
        """
        `Extended QPanda API` \n
        Free a list of qubit \n
        list<Qubit> -> None
        """
        for q in qubit_list:
            self.qFree(q)   

    def cFree_all(self, cbit_list):
        """
        `Extended QPanda API` \n
        Free a list of cbit \n
        list<CBit> -> None
        """
        for c in cbit_list:
            self.cFree(c)

    def directly_run(self, QProg=None):
        """
        `Extended QPanda API` \n
        Load, Run and Fetch Result \n
        QProg(optional) -> Dict<string,bool> \n
        Comment: if called by `directly_run()`, it will use the loaded program,
        if called by `directly_run(qprog)`, the input QProg will be loaded first
        """
        if QProg is None:
            self.run()
            return self.getResultMap()
        else:
            self.load(QProg)
            self.run()
            return self.getResultMap()

    def result_to_binary_string(self, cbit_list):
        """
        `Extended QPanda API` \n
        Turn the cbits (after running) into 0/1 string \n
        list<CBit> -> string
        """
        result_str=''
        for c in cbit_list:
            if self.getCBitValue(c):
                result_str=result_str+'1'
            else:
                result_str=result_str+'0'
        
        return result_str
    
    def get_prob(self, qlist, select_max=-1, listonly=False):
        '''
        `QPanda Basic API`
        get the probabilities distribution
        select_max(optional): select the biggest `select_max` probs.

        list<Qubit>, int -> list<tuple<int,double> (listonly=False)
        list<Qubit> -> list<double> (listonly=True)
        '''

        from pyqpanda import pyQPanda

        if listonly is False:              
            return pyQPanda.PMeasure_QMachine(self._quantum_machine,qlist,select_max)
        else:       
            return pyQPanda.PMeasure_no_index_QMachine(self._quantum_machine,qlist)

    def get_probabilites(self, qlist, select_max=-1, dataType="dict"):
        '''
        `QPanda Extended API`
        Get the select_max (default -1 for all distribution) largest
        component from the probability distribution with qubits (qlist)

        list<Qubit>, int(optional) ->  dict<string,double> (dataType="dict")
        list<Qubit>, int(optional) ->  list<tuple<int,double> (dataType="tuplelist")
        list<Qubit>, int(optional) ->  list<double> (dataType="list")
        '''
        max_digit=len(qlist)
        if dataType == "dict":        
            prob=self.get_prob(qlist,select_max)
            probabilites=dict()
            for pair in prob:
                probabilites[(pywrap.dec2bin(pair[0],max_digit))]=pair[1]
            return probabilites
        elif dataType == "tuplelist":        
            prob=self.get_prob(qlist,select_max)
            return prob
        elif dataType == "list":
            prob=self.get_prob(qlist,select_max, True)
            return prob
        else:
            assert False        

    def prob_run(
        self,
        program=None,
        noise=False,
        select_max=-1,
        qubit_list=[],
        dataType= 'tuplelist'
    ):
        '''
        `Extended QPanda API
        '''
        if noise:
            raise("Noisy simulation is not implemented yet")
        
        if program is not None:
            self.load(program)

        self.run()
        return self.get_probabilites(qlist=qubit_list,select_max=select_max,dataType=dataType)

    def run_with_configuration(
        self,
        program=None,
        shots=100,
        noise=False,
        cbit_list={}
    ):
        """
        `Extended QPanda API`
            Run the program with some configuration
            Args:
                prog(optional): assign the program to run
                shots: repeated time of running
                noise:  True=Simulation with noise
                        False=Noise Free Simulation
                cbit_list: the CBit value you care
            Return:
                (shots=0) dict<string,bool>
                (otherwise) dict<string,int>
            Comments:
                1. If shots=0, it is same directly_run
                2. Noisy simulation is not implemented yet
                3. Assigning a prog means the loaded program will be overwritten
        """
        if noise:
            raise("Noisy simulation is not implemented yet")

        if program is not None:
            self.load(program)
        
        if shots==0:
            if cbit_list=={}:
                return self.directly_run()
            else:
                print("**************************************************************************")
                print("WARNING: In 'run_with_configuration' the param 'cbit_list' will be ignored")
                print("  CAUSE: shots==0")
                print("**************************************************************************")
                return self.directly_run()
        else:
            result_dict=dict()
            for i in range(0,shots):
                self.run()
                s=self.result_to_binary_string(cbit_list)
                if not s in result_dict:
                    result_dict[s]=1
                else:
                    result_dict[s]=result_dict[s]+1
            return result_dict         

    def quick_measure(self, qlist, shots,seed=None, use_cpp=True):
        '''
        a fast way for sampling.
        after run the program without measurement, call this to fetch
        a simulated result of many shots.

        qlist: qubits to measure
        shots: execution times
        seed(optional) : choose random seed
        use_cpp: use C++ version instead of a python one

        list<Qubit>, int -> dict<string, int>
        '''
        prob_list=self.get_prob(qlist,listonly=True)    
        accumulate_prob=pywrap.accumulate_probabilities(prob_list)
        
        if use_cpp is False:
            meas_result=dict()

            for i in range(shots):    
                rnd=random.random()        
                # direct search
                if rnd<accumulate_prob[0]:            
                    pywrap.add_up_a_dict(meas_result,
                                pywrap.dec2bin(0,len(qlist)))
                    continue

                for i in range(1,len(accumulate_prob)):
                    if rnd<accumulate_prob[i] and rnd>=accumulate_prob[i-1]:                
                        pywrap.add_up_a_dict(meas_result,pywrap.dec2bin(i,len(qlist)))
                        break  
        else:
            meas_result=pywrap.quick_measure_cpp(qlist, shots, accumulate_prob)

        return meas_result   