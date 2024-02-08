import unittest
import time
import platform
import smbus
from saa1064driver import SevenSegmentDisplay

QuadAddressMap = [0x38,0x39,0x3a,0x3b]
QuadDigitMap =[[1, 2, 3, 4],[2, 1, 4, 3],[4, 3, 2, 1],[1, 2, 3, 4]]


BLANK_DIGIT = 0x00
DP_ONLY = 0x01
ZERO_WITHOUT_DP = 0x7E
ONE_WITHOUT_DP = 0x0C
TWO_WITHOUT_DP = 0xB6
THREE_WITHOUT_DP = 0x9E
FOUR_WITHOUT_DP = 0xCC
FIVE_WITHOUT_DP = 0xDA
NINE_WITHOUT_DP = 0xDE
b_WITHOUT_DP = 0xF8
d_WITHOUT_DP = 0xBC
NEG_WITHOUT_DP = 0x80
POS_WITHOUT_DP = 0x84


ZERO_WITH_DP = 0x7F
ONE_WITH_DP = 0x0D
FIVE_WITH_DP = 0xDB



class TestStringMethods(unittest.TestCase):

    def setUp(self):
        bus = smbus.SMBus(1)
        bus.resetAllDevices()

    #def tearDown(self):
    
    # UNIT TEST HELPERS
    def check4Digits(self,displayObject,addressToUse,QuadDigitMapToUse,digit4,digit3,digit2,digit1):
        bus = smbus.SMBus(1)
        self.assertEqual(bus.read_byte_data(addressToUse,0x01), digit1)
        self.assertEqual(bus.read_byte_data(addressToUse,0x02), digit2)
        self.assertEqual(bus.read_byte_data(addressToUse,0x03), digit3)
        self.assertEqual(bus.read_byte_data(addressToUse,0x04), digit4)

    def test_a_display_control_mode_initialised_to_dynamic_with_digits_1_to_4(self):     
        bus = smbus.SMBus(1)
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        notUsed = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse) 
        self.assertEqual(bus.read_byte_data(addressToUse,0x00), 0x17)
        
    def test_b_display_is_cleared_on_intialisation(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,0x00,0x00,0x00,0x00)
    
    def test_c_display_clear_digit_seperately(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(1234)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,ONE_WITHOUT_DP,TWO_WITHOUT_DP,THREE_WITHOUT_DP,FOUR_WITHOUT_DP)
        display1.clear_digit(2)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,ONE_WITHOUT_DP,TWO_WITHOUT_DP,0x00,FOUR_WITHOUT_DP)
        display1.clear_digit(3)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,ONE_WITHOUT_DP,0x00,0x00,FOUR_WITHOUT_DP)
        display1.clear_digit(4)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,0x00,0x00,0x00,FOUR_WITHOUT_DP)
        display1.clear_digit(1)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,0x00,0x00,0x00,0x00)
        
    def test_d_display_clear_all_digits(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(1234)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,ONE_WITHOUT_DP,TWO_WITHOUT_DP,THREE_WITHOUT_DP,FOUR_WITHOUT_DP)
        display1.clear_all_digits()
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,0x00,0x00,0x00,0x00)      
        
    # int specific tests
    def test_e_display_write_number_given_as_int_correctly(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]	
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(1111)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,ONE_WITHOUT_DP,ONE_WITHOUT_DP,ONE_WITHOUT_DP,ONE_WITHOUT_DP)


    def test_e_display_write_number_given_negative_displays_negative_sign(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(-999)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,NEG_WITHOUT_DP,NINE_WITHOUT_DP,NINE_WITHOUT_DP,NINE_WITHOUT_DP)
        
    def test_e_display_write_number_given_postive_char_displays_pseudo_pos(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_str_number("+999")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,POS_WITHOUT_DP,NINE_WITHOUT_DP,NINE_WITHOUT_DP,NINE_WITHOUT_DP)
        
    def test_e_display_write_number_given_too_large_negative_displays_negative_limit_value(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(-9999)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,NEG_WITHOUT_DP,NINE_WITHOUT_DP,NINE_WITHOUT_DP,NINE_WITHOUT_DP)


    def test_f_display_write_number_same_digits_doesnt_result_in_i2c_transmission(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        bus = smbus.SMBus(1)
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        bus.resetWriteFlag()
        display1.write_number(1111)
        self.assertTrue(bus.getWriteFlagStatus())
        bus.resetWriteFlag()
        display1.write_number(1111)  
        self.assertFalse(bus.getWriteFlagStatus())
        
    # string specific tests
    def test_g_display_write_number_given_as_string(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number("2222")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,TWO_WITHOUT_DP,TWO_WITHOUT_DP,TWO_WITHOUT_DP,TWO_WITHOUT_DP)
        
        
    def test_h_display_write_number_dps_only(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number("....")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,DP_ONLY,DP_ONLY,DP_ONLY,DP_ONLY)
        
    def test_i_display_write_number_digits_with_multiple_dps(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number("5.5.5.5.")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,FIVE_WITH_DP,FIVE_WITH_DP,FIVE_WITH_DP,FIVE_WITH_DP)
        
        display1.write_number("5.5.")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,BLANK_DIGIT,FIVE_WITH_DP,FIVE_WITH_DP)
        
        display1.write_number("5...5.")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,FIVE_WITH_DP,DP_ONLY,DP_ONLY,FIVE_WITH_DP)
        
        display1.write_number("5...")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,FIVE_WITH_DP,DP_ONLY,DP_ONLY)
        
        display1.write_number("...5")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,DP_ONLY,DP_ONLY,DP_ONLY,FIVE_WITHOUT_DP)
        
        display1.write_number("55..")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,FIVE_WITHOUT_DP,FIVE_WITH_DP,DP_ONLY)
        
        display1.write_number("  . ")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,BLANK_DIGIT,DP_ONLY,BLANK_DIGIT)
        
        display1.write_number("   .")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,BLANK_DIGIT,BLANK_DIGIT,DP_ONLY)
    
    def test_j_display_write_number_with_unsupported_characters_replaces_with_spaces(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number("abcd")
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,b_WITHOUT_DP,BLANK_DIGIT,d_WITHOUT_DP)
    
    # float specific tests
    def test_k_display_write_number_given_as_float(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(1.111)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,ONE_WITH_DP,ONE_WITHOUT_DP,ONE_WITHOUT_DP,ONE_WITHOUT_DP)
        
    def test_l_display_write_zero_as_float(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(0.000)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,BLANK_DIGIT,ZERO_WITH_DP,ZERO_WITHOUT_DP)    
        
    def test_m_display_writing_negative_float_becomes_zero_point_zero(self):
        quadToUse = 1
        addressToUse =  QuadAddressMap[quadToUse-1]    
        QuadDigitMapToUse = QuadDigitMap[quadToUse-1]
        
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
        display1.write_number(-1.000)
        self.check4Digits(display1,addressToUse,QuadDigitMapToUse,BLANK_DIGIT,BLANK_DIGIT,ZERO_WITH_DP,ZERO_WITHOUT_DP)    
        
if __name__ == '__main__':
    unittest.main()
