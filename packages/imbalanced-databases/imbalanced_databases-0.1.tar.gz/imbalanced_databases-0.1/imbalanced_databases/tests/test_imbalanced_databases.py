#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:45:08 2018

@author: gykovacs
"""

import imbalanced_databases as imbd

def read_and_validate(name):
    """
    Tests the dimensions of the datasets
    Args:
        name (str): the name of the dataset
    """
    data_0= descriptors[name][0](return_X_y= False, encode= False)
    data_1= descriptors[name][0](return_X_y= True, encode= False)
    data_2= descriptors[name][0](return_X_y= False, encode= True)
    data_3= descriptors[name][0](return_X_y= True, encode= True)
    
    assert len(data_0['data']) == len(data_1[0])
    assert len(data_0['data']) == len(data_2['data'])
    assert len(data_0['data']) == len(data_3[0])
    
    assert len(data_0['data'][0]) == len(data_1[0][0])
    assert len(data_0['data'][0]) <= len(data_2['data'][0])
    assert len(data_0['data'][0]) <= len(data_3[0][0])

def test_ada(): read_and_validate('ada')
    
def test_cm1(): read_and_validate('cm1')

def test_german(): read_and_validate('german')
    
def test_glass(): read_and_validate('glass')
    
def test_hepatitis(): read_and_validate('hepatitis')
    
def test_hiva(): read_and_validate('hiva')
    
def test_hypothyroid(): read_and_validate('hypothyroid')
    
def test_kc1(): read_and_validate('kc1')
    
def test_pc1(): read_and_validate('pc1')
    
def test_satimage(): read_and_validate('satimage')
    
def test_spect_f(): read_and_validate('spect_f')
    
def test_sylva(): read_and_validate('sylva')
    
def test_vehicle(): read_and_validate('vehicle')
    
