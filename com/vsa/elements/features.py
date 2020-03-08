# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:47:10 2019

@author: ACE
"""

from com.vsa.elements.Operators import Operators
from com.vsa.elements.Operands import Operands
from com.vsa.language_model.ngram.ngram import NGram

from itertools import permutations
#from sympy.combinatorics.permutations import Permutation

class Features:
    
    
    public = 'public'
    private = 'private'
    protected = 'protected'
    
    classes = 'class'
    abstract = 'abstract'
    interface = 'interface'
    
    extends = 'extends'
    implements = 'implements'
    
    try_feature = 'try'
    catch = 'catch'
    finally_feature = 'finally'
    throw = 'throw'
    throws = 'throws'
    
    void  =  'void'
    static = 'static'
    final = 'final'
    finalize = 'finalize'
    import_feature = 'import'
    
    curly_bracket_right = '}'
    curly_bracket_left = '{'
    round_bracket_right = ')'
    round_bracket_left = '('
    straight_bracket_left = '['
    straight_bracket_right = ']'
    
    for_loop = 'for'
    while_loop = 'while'
    do_while_lopp = 'do'
    break_feature = 'break'
    continue_feature = 'continue'
    switch_case = 'switch'
    case = 'case'
    default = 'default'
    if_feature = 'if'
    else_feature = 'else'
    
    this='this'
    
    features = [public,private,protected,classes,abstract,interface,
               extends,implements,try_feature,catch,finally_feature,
               throw,throws,void,static,final,finalize,import_feature,
               curly_bracket_left,curly_bracket_right,round_bracket_left,
               round_bracket_right,straight_bracket_left,straight_bracket_right,
               for_loop,while_loop,do_while_lopp,break_feature,continue_feature,
               switch_case,case,default,if_feature,else_feature,this]

    '''
    operators
    '''
    
    operators = []
    operators.extend(Operators.arthmetic_op)
    operators.extend(Operators.logical_op)
    
    '''
    operands
    '''
    
    operands = []
    operands.extend(Operands.operands_list)
    
    
    features.extend(operands)
    features.extend(operators)    
    

    def get_feature_combinations(features, n=1):
        '''
        features_str=NGram.list_to_string(NGram,features)
        list.reverse(features)
        features_str_re=NGram.list_to_string(NGram,features)
        tokenize_words = NGram.tokenize(NGram,features_str)
        tokenize_words += NGram.tokenize(NGram,features_str_re)
        return[x for x in NGram.n_gram(NGram,tokenize_words,n)]
        '''
       
        
        return [x for x in permutations(features,n)]
    

        
if __name__ == '__main__':
   # print(Features.features)
   # t=Features.get_feature_combinations(Features.features,2)
   # print(t[0].__str__().upper())
    list.reverse(Features.features)
    print(Features.features)
    
    