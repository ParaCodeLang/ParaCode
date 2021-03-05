from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.variable import VariableType
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction
from interpreter.env.builtins import *

class Globals:
    def __init__(self):
        self.basic_type = BasicType(
            None,
            {
                'name': BasicValue('Type'),
                'extend': BuiltinFunction('Type.extend', None, builtin_type_extend),
                # 'type': BuiltinFunction('Type.type', None, builtin_type_type),
                # 'is': BuiltinFunction('Type.is', None, builtin_type_is),
                'to_str': BuiltinFunction('Type.to_str', None, builtin_type_to_str),
                # 'new': BuiltinFunction('Object.new', None, builtin_object_new),
            },
            True
        )
        self.basic_object = BasicType(
            self.basic_type,
            {
                'instance': BasicObject(members={}),
                'name': BasicValue('Object'),
                'new': BuiltinFunction('Object.new', None, builtin_object_new),
                'type': BuiltinFunction('Object.type', None, builtin_object_type),
                'is': BuiltinFunction('Object.is', None, builtin_object_is),
                'to_str': BuiltinFunction('Object.to_str', None, builtin_object_to_str)
            }
        )

        self.basic_type.parent = self.basic_object # circular

        self.func_type = BasicType(
            self.basic_type,
            {
                'name': BasicValue('Func'),
                'instance': BasicObject(members={})
            }
        )

        self.variables = [
            ('Type', VariableType.Object, self.basic_type),
            ('Object', VariableType.Type, self.basic_object),
            ('Func', VariableType.Type, self.func_type),
            ('__intern_object_patch__', VariableType.Function, BuiltinFunction("__intern_object_patch__", None, builtin_object_patch)),
            ('__intern_math_max__', VariableType.Function, BuiltinFunction("__intern_math_max__", None, builtin_math_max)),
            ('__intern_math_min__', VariableType.Function, BuiltinFunction("__intern_math_min__", None, builtin_math_min)),
            ('__intern_print__', VariableType.Function, BuiltinFunction("__intern_print__", None, builtin_printn)),
            ('__intern_console_write__', VariableType.Function, BuiltinFunction("__intern_console_write__", None, builtin_console_write)),
            ('__intern_print_color__', VariableType.Function, BuiltinFunction("__intern_print_color__", None, builtin_print_color)),
            ('__intern_type_compare__', VariableType.Function, BuiltinFunction("__intern_type_compare__", None, builtin_type_compare)),
            ('__intern_default_compare__', VariableType.Function, BuiltinFunction("__intern_default_compare__", None, builtin_default_compare)),
            ('__intern_int_negate__', VariableType.Function, BuiltinFunction("__intern_int_negate__", None, builtin_int_negate)),
            ('__intern_varinfo__', VariableType.Function, BuiltinFunction("__intern_varinfo__", None, builtin_varinfo)),
            ('__intern_exit__', VariableType.Function, BuiltinFunction("__intern_exit__", None, builtin_exit)),
            ('__intern_to_int__', VariableType.Function, BuiltinFunction("__intern_to_int__", None, builtin_to_int)),
            ('__intern_to_float__', VariableType.Function, BuiltinFunction("__intern_to_float__", None, builtin_to_float)),
            ('__intern_num_to_str__', VariableType.Function, BuiltinFunction("__intern_num_to_str__", None, builtin_num_to_str)),
            ('__intern_str_len__', VariableType.Function, BuiltinFunction("__intern_str_len__", None, builtin_str_len)),
            ('__intern_str_append__', VariableType.Function, BuiltinFunction("__intern_str_append__", None, builtin_str_append)),
						('__intern_str_replace__', VariableType.Function, BuiltinFunction("__intern_str_replace__", None, builtin_str_replace)),
						('__intern_str_tolower__', VariableType.Function, BuiltinFunction("__intern_str_tolower__", None, builtin_str_tolower)),
						('__intern_str_toupper__', VariableType.Function, BuiltinFunction("__intern_str_toupper__", None, builtin_str_toupper)),

            ('__intern_eval__', VariableType.Function, BuiltinFunction("__intern_eval__", None, builtin_eval)),

            ('__intern_array_len__', VariableType.Function, BuiltinFunction("__intern_array_len__", None, builtin_array_len)),
            ('__intern_array_at__', VariableType.Function, BuiltinFunction("__intern_array_at__", None, builtin_array_at)),
            ('__intern_array_append__', VariableType.Function, BuiltinFunction("__intern_array_append__", None, builtin_array_append)),
            ('__intern_array_set__', VariableType.Function, BuiltinFunction("__intern_array_set__", None, builtin_array_set)),
            ('__intern_array_clone__', VariableType.Function, BuiltinFunction("__intern_array_clone__", None, builtin_array_clone)),

            ('__intern_dictionary_len__', VariableType.Function, BuiltinFunction("__intern_dictionary_len__", None, builtin_dictionary_len)),
            ('__intern_dictionary_at__', VariableType.Function, BuiltinFunction("__intern_dictionary_at__", None, builtin_dictionary_at)),
            ('__intern_dictionary_append__', VariableType.Function, BuiltinFunction("__intern_dictionary_append__", None, builtin_dictionary_append)),
            ('__intern_dictionary_set__', VariableType.Function, BuiltinFunction("__intern_dictionary_set__", None, builtin_dictionary_set)),
            ('__intern_dictionary_clone__', VariableType.Function, BuiltinFunction("__intern_dictionary_clone__", None, builtin_dictionary_clone)),
            
            ('__intern_console_input__', VariableType.Function, BuiltinFunction("__intern_console_input__", None, builtin_console_input)),
            ('__intern_file_read__', VariableType.Function, BuiltinFunction("__intern_file_read__", None, builtin_file_read)),
            ('__intern_file_readlines__', VariableType.Function, BuiltinFunction("__intern_file_readlines__", None, builtin_file_readlines)),
            ('__intern_file_write__', VariableType.Function, BuiltinFunction("__intern_file_write__", None, builtin_file_write)),
            ('__intern_file_append__', VariableType.Function, BuiltinFunction("__intern_file_append__", None, builtin_file_append)),
            ('__intern_file_create__', VariableType.Function, BuiltinFunction("__intern_file_create__", None, builtin_file_create)),
            ('__intern_file_delete__', VariableType.Function, BuiltinFunction("__intern_file_delete__", None, builtin_file_delete)),
            ('__intern_file_deletedir__', VariableType.Function, BuiltinFunction("__intern_file_deletedir__", None, builtin_file_deletedir)),
            ('__intern_file_exists__', VariableType.Function, BuiltinFunction("__intern_file_exists__", None, builtin_file_exists)),
            ('__intern_is_file__', VariableType.Function, BuiltinFunction("__intern_is_file__", None, builtin_is_file)),
            ('__intern_is_dir__', VariableType.Function, BuiltinFunction("__intern_is_dir__", None, builtin_is_dir)),

            ('__intern_json_load__', VariableType.Function, BuiltinFunction("__intern_json_load__", None, builtin_json_load)),
            ('__intern_json_loads__', VariableType.Function, BuiltinFunction("__intern_json_loads__", None, builtin_json_loads)),
            ('__intern_json_dump__', VariableType.Function, BuiltinFunction("__intern_json_dump__", None, builtin_json_dump)),
            ('__intern_json_dumps__', VariableType.Function, BuiltinFunction("__intern_json_dumps__", None, builtin_json_dumps)),
            
            ('__intern_numpara_mean__', VariableType.Function, BuiltinFunction("__intern_numpara_mean__", None, builtin_numpara_mean)),
            ('__intern_numpara_median__', VariableType.Function, BuiltinFunction("__intern_numpara_median__", None, builtin_numpara_median)),

            ('__intern_scipara_mean__', VariableType.Function, BuiltinFunction("__intern_scipara_mean__", None, builtin_scipara_mean)),
            ('__intern_scipara_median__', VariableType.Function, BuiltinFunction("__intern_scipara_median__", None, builtin_scipara_median)),
            ('__intern_scipara_mode__', VariableType.Function, BuiltinFunction("__intern_scipara_mode__", None, builtin_scipara_mode)),
            ('__intern_scipara_getliter__', VariableType.Function, BuiltinFunction("__intern_scipara_getliter__", None, builtin_scipara_getliter)),
            ('__intern_scipara_getpi__', VariableType.Function, BuiltinFunction("__intern_scipara_getpi__", None, builtin_scipara_getpi)),
            ('__intern_scipara_getyotta__', VariableType.Function, BuiltinFunction("__intern_scipara_getyotta__", None, builtin_scipara_getyotta)),
            ('__intern_scipara_getzetta__', VariableType.Function, BuiltinFunction("__intern_scipara_getzetta__", None, builtin_scipara_getzetta)),
            ('__intern_scipara_getexa__', VariableType.Function, BuiltinFunction("__intern_scipara_getexa__", None, builtin_scipara_getexa)),
            ('__intern_scipara_getpeta__', VariableType.Function, BuiltinFunction("__intern_scipara_getpeta__", None, builtin_scipara_getpeta)),
            ('__intern_scipara_gettera__', VariableType.Function, BuiltinFunction("__intern_scipara_gettera__", None, builtin_scipara_gettera)),
            ('__intern_scipara_getgiga__', VariableType.Function, BuiltinFunction("__intern_scipara_getgiga__", None, builtin_scipara_getgiga)),
            ('__intern_scipara_getmega__', VariableType.Function, BuiltinFunction("__intern_scipara_getmega__", None, builtin_scipara_getmega)),
            ('__intern_scipara_getkilo__', VariableType.Function, BuiltinFunction("__intern_scipara_getkilo__", None, builtin_scipara_getkilo)),
            ('__intern_scipara_gethecto__', VariableType.Function, BuiltinFunction("__intern_scipara_gethecto__", None, builtin_scipara_gethecto)),
            ('__intern_scipara_getdeka__', VariableType.Function, BuiltinFunction("__intern_scipara_getdeka__", None, builtin_scipara_getdeka)),
            ('__intern_scipara_getdeci__', VariableType.Function, BuiltinFunction("__intern_scipara_getdeci__", None, builtin_scipara_getdeci)),
            ('__intern_scipara_getcenti__', VariableType.Function, BuiltinFunction("__intern_scipara_getcenti__", None, builtin_scipara_getcenti)),
            ('__intern_scipara_getmilli__', VariableType.Function, BuiltinFunction("__intern_scipara_getmilli__", None, builtin_scipara_getmilli)),
            ('__intern_scipara_getmicro__', VariableType.Function, BuiltinFunction("__intern_scipara_getmicro__", None, builtin_scipara_getmicro)),
            ('__intern_scipara_getnano__', VariableType.Function, BuiltinFunction("__intern_scipara_getnano__", None, builtin_scipara_getnano)),
            ('__intern_scipara_getpico__', VariableType.Function, BuiltinFunction("__intern_scipara_getpico__", None, builtin_scipara_getpico)),
            ('__intern_scipara_getfemto__', VariableType.Function, BuiltinFunction("__intern_scipara_getfemto__", None, builtin_scipara_getfemto)),
            ('__intern_scipara_getatto__', VariableType.Function, BuiltinFunction("__intern_scipara_getatto__", None, builtin_scipara_getatto)),
            ('__intern_scipara_getzepto__', VariableType.Function, BuiltinFunction("__intern_scipara_getzepto__", None, builtin_scipara_getzepto)),
            ('__intern_scipara_getkibi__', VariableType.Function, BuiltinFunction("__intern_scipara_getkibi__", None, builtin_scipara_getkibi)),
            ('__intern_scipara_getmebi__', VariableType.Function, BuiltinFunction("__intern_scipara_getmebi__", None, builtin_scipara_getmebi)),
            ('__intern_scipara_getgibi__', VariableType.Function, BuiltinFunction("__intern_scipara_getgibi__", None, builtin_scipara_getgibi)),
            ('__intern_scipara_gettebi__', VariableType.Function, BuiltinFunction("__intern_scipara_gettebi__", None, builtin_scipara_gettebi)),
            ('__intern_scipara_getpebi__', VariableType.Function, BuiltinFunction("__intern_scipara_getpebi__", None, builtin_scipara_getpebi)),
            ('__intern_scipara_getexbi__', VariableType.Function, BuiltinFunction("__intern_scipara_getexbi__", None, builtin_scipara_getexbi)),
            ('__intern_scipara_getzebi__', VariableType.Function, BuiltinFunction("__intern_scipara_getzebi__", None, builtin_scipara_getzebi)),
            ('__intern_scipara_getyobi__', VariableType.Function, BuiltinFunction("__intern_scipara_getyobi__", None, builtin_scipara_getyobi)),
            ('__intern_scipara_getgram__', VariableType.Function, BuiltinFunction("__intern_scipara_getgram__", None, builtin_scipara_getgram)),
            ('__intern_scipara_getmetric_ton__', VariableType.Function, BuiltinFunction("__intern_scipara_getmetric_ton__", None, builtin_scipara_getmetric_ton)),
            ('__intern_scipara_getgrain__', VariableType.Function, BuiltinFunction("__intern_scipara_getgrain__", None, builtin_scipara_getgrain)),
            ('__intern_scipara_getlb__', VariableType.Function, BuiltinFunction("__intern_scipara_getlb__", None, builtin_scipara_getlb)),
            ('__intern_scipara_getpound__', VariableType.Function, BuiltinFunction("__intern_scipara_getpound__", None, builtin_scipara_getpound)),
            ('__intern_scipara_getoz__', VariableType.Function, BuiltinFunction("__intern_scipara_getoz__", None, builtin_scipara_getoz)),
            ('__intern_scipara_getounce__', VariableType.Function, BuiltinFunction("__intern_scipara_getounce__", None, builtin_scipara_getounce)),
            ('__intern_scipara_getstone__', VariableType.Function, BuiltinFunction("__intern_scipara_getstone__", None, builtin_scipara_getstone)),
            ('__intern_scipara_getlong_ton__', VariableType.Function, BuiltinFunction("__intern_scipara_getlong_ton__", None, builtin_scipara_getlong_ton)),
            ('__intern_scipara_getshort_ton__', VariableType.Function, BuiltinFunction("__intern_scipara_getshort_ton__", None, builtin_scipara_getshort_ton)),
            ('__intern_scipara_gettroy_ounce__', VariableType.Function, BuiltinFunction("__intern_scipara_gettroy_ounce__", None, builtin_scipara_gettroy_ounce)),
            ('__intern_scipara_gettroy_pound__', VariableType.Function, BuiltinFunction("__intern_scipara_gettroy_pound__", None, builtin_scipara_gettroy_pound)),
            ('__intern_scipara_getcarat__', VariableType.Function, BuiltinFunction("__intern_scipara_getcarat__", None, builtin_scipara_getcarat)),
            ('__intern_scipara_getatomic_mass__', VariableType.Function, BuiltinFunction("__intern_scipara_getatomic_mass__", None, builtin_scipara_getatomic_mass)),
            ('__intern_scipara_getm_u__', VariableType.Function, BuiltinFunction("__intern_scipara_getm_u__", None, builtin_scipara_getm_u)),
            ('__intern_scipara_getu__', VariableType.Function, BuiltinFunction("__intern_scipara_getu__", None, builtin_scipara_getu)),
            ('__intern_scipara_getdegree__', VariableType.Function, BuiltinFunction("__intern_scipara_getdegree__", None, builtin_scipara_getdegree)),
            ('__intern_scipara_getarcmin__', VariableType.Function, BuiltinFunction("__intern_scipara_getarcmin__", None, builtin_scipara_getarcmin)),
            ('__intern_scipara_getarcminute__', VariableType.Function, BuiltinFunction("__intern_scipara_getarcminute__", None, builtin_scipara_getarcminute)),
            ('__intern_scipara_getarcsec__', VariableType.Function, BuiltinFunction("__intern_scipara_getarcsec__", None, builtin_scipara_getarcsec)),
            ('__intern_scipara_getarcsecond__', VariableType.Function, BuiltinFunction("__intern_scipara_getarcsecond__", None, builtin_scipara_getarcsecond)),
            ('__intern_scipara_getminute__', VariableType.Function, BuiltinFunction("__intern_scipara_getminute__", None, builtin_scipara_getminute)),
            ('__intern_scipara_gethour__', VariableType.Function, BuiltinFunction("__intern_scipara_gethour__", None, builtin_scipara_gethour)),
            ('__intern_scipara_getday__', VariableType.Function, BuiltinFunction("__intern_scipara_getday__", None, builtin_scipara_getday)),
            ('__intern_scipara_getweek__', VariableType.Function, BuiltinFunction("__intern_scipara_getweek__", None, builtin_scipara_getweek)),
            ('__intern_scipara_getyear__', VariableType.Function, BuiltinFunction("__intern_scipara_getyear__", None, builtin_scipara_getyear)),
            ('__intern_scipara_getJulian_year__', VariableType.Function, BuiltinFunction("__intern_scipara_getJulian_year__", None, builtin_scipara_getJulian_year)),
            ('__intern_scipara_getinch__', VariableType.Function, BuiltinFunction("__intern_scipara_getinch__", None, builtin_scipara_getinch)),
            ('__intern_scipara_getfoot__', VariableType.Function, BuiltinFunction("__intern_scipara_getfoot__", None, builtin_scipara_getfoot)),
            ('__intern_scipara_getyard__', VariableType.Function, BuiltinFunction("__intern_scipara_getyard__", None, builtin_scipara_getyard)),
            ('__intern_scipara_getmile__', VariableType.Function, BuiltinFunction("__intern_scipara_getmile__", None, builtin_scipara_getmile)),
            ('__intern_scipara_getmil__', VariableType.Function, BuiltinFunction("__intern_scipara_getmil__", None, builtin_scipara_getmil)),
            ('__intern_scipara_getpt__', VariableType.Function, BuiltinFunction("__intern_scipara_getpt__", None, builtin_scipara_getpt)),
            ('__intern_scipara_getpoint__', VariableType.Function, BuiltinFunction("__intern_scipara_getpoint__", None, builtin_scipara_getpoint)),
            ('__intern_scipara_getsurvey_foot__', VariableType.Function, BuiltinFunction("__intern_scipara_getsurvey_foot__", None, builtin_scipara_getsurvey_foot)),
            ('__intern_scipara_getsurvey_mile__', VariableType.Function, BuiltinFunction("__intern_scipara_getsurvey_mile__", None, builtin_scipara_getsurvey_mile)),
            ('__intern_scipara_getnautical_mile__', VariableType.Function, BuiltinFunction("__intern_scipara_getnautical_mile__", None, builtin_scipara_getnautical_mile)),
            ('__intern_scipara_getfermi__', VariableType.Function, BuiltinFunction("__intern_scipara_getfermi__", None, builtin_scipara_getfermi)),
            ('__intern_scipara_getangstrom__', VariableType.Function, BuiltinFunction("__intern_scipara_getangstrom__", None, builtin_scipara_getangstrom)),
            ('__intern_scipara_getmicron__', VariableType.Function, BuiltinFunction("__intern_scipara_getmicron__", None, builtin_scipara_getmicron)),
            ('__intern_scipara_getau__', VariableType.Function, BuiltinFunction("__intern_scipara_getau__", None, builtin_scipara_getau)),
            ('__intern_scipara_getastronomical_unit__', VariableType.Function, BuiltinFunction("__intern_scipara_getastronomical_unit__", None, builtin_scipara_getastronomical_unit)),
            ('__intern_scipara_getlight_year__', VariableType.Function, BuiltinFunction("__intern_scipara_getlight_year__", None, builtin_scipara_getlight_year)),
            ('__intern_scipara_getparsec__', VariableType.Function, BuiltinFunction("__intern_scipara_getparsec__", None, builtin_scipara_getparsec)),
            ('__intern_scipara_getatm__', VariableType.Function, BuiltinFunction("__intern_scipara_getatm__", None, builtin_scipara_getatm)),
            ('__intern_scipara_getatmosphere__', VariableType.Function, BuiltinFunction("__intern_scipara_getatmosphere__", None, builtin_scipara_getatmosphere)),
            ('__intern_scipara_getbar__', VariableType.Function, BuiltinFunction("__intern_scipara_getbar__", None, builtin_scipara_getbar)),
            ('__intern_scipara_gettorr__', VariableType.Function, BuiltinFunction("__intern_scipara_gettorr__", None, builtin_scipara_gettorr)),
            ('__intern_scipara_getmmHg__', VariableType.Function, BuiltinFunction("__intern_scipara_getmmHg__", None, builtin_scipara_getmmHg)),
            ('__intern_scipara_getpsi__', VariableType.Function, BuiltinFunction("__intern_scipara_getpsi__", None, builtin_scipara_getpsi)),
            ('__intern_scipara_gethectare__', VariableType.Function, BuiltinFunction("__intern_scipara_gethectare__", None, builtin_scipara_getectare)),
            ('__intern_scipara_getacre__', VariableType.Function, BuiltinFunction("__intern_scipara_getacre__", None, builtin_scipara_getacre)),
            ('__intern_scipara_getliter__', VariableType.Function, BuiltinFunction("__intern_scipara_getliter__", None, builtin_scipara_getliter)),
            ('__intern_scipara_getlitre__', VariableType.Function, BuiltinFunction("__intern_scipara_getlitre__", None, builtin_scipara_getlitre)),
            ('__intern_scipara_getgallon__', VariableType.Function, BuiltinFunction("__intern_scipara_getgallon__", None, builtin_scipara_getgallon)),
            ('__intern_scipara_getgallon_US__', VariableType.Function, BuiltinFunction("__intern_scipara_getgallon_US__", None, builtin_scipara_getgallon_US)),
            ('__intern_scipara_getgallon_imp__', VariableType.Function, BuiltinFunction("__intern_scipara_getgallon_imp__", None, builtin_scipara_getgallon_imp)),
            ('__intern_scipara_getfluid_ounce__', VariableType.Function, BuiltinFunction("__intern_scipara_getfluid_ounce__", None, builtin_scipara_getfluid_ounce)),
            ('__intern_scipara_getfluid_ounce_US__', VariableType.Function, BuiltinFunction("__intern_scipara_getfluid_ounce_US__", None, builtin_scipara_getfluid_ounce_US)),
            ('__intern_scipara_getfluid_ounce_imp__', VariableType.Function, BuiltinFunction("__intern_scipara_getfluid_ounce_imp__", None, builtin_scipara_getfluid_ounce_imp)),
            ('__intern_scipara_getbarrel__', VariableType.Function, BuiltinFunction("__intern_scipara_getbarrel__", None, builtin_scipara_getbarrel)),
            ('__intern_scipara_getbbl__', VariableType.Function, BuiltinFunction("__intern_scipara_getbbl__", None, builtin_scipara_getbbl)),
            ('__intern_scipara_getkmh__', VariableType.Function, BuiltinFunction("__intern_scipara_getkmh__", None, builtin_scipara_getkmh)),
            ('__intern_scipara_getmph__', VariableType.Function, BuiltinFunction("__intern_scipara_getmph__", None, builtin_scipara_getmph)),
            ('__intern_scipara_getmach__', VariableType.Function, BuiltinFunction("__intern_scipara_getmach__", None, builtin_scipara_getmach)),
            ('__intern_scipara_getspeed_of_sound__', VariableType.Function, BuiltinFunction("__intern_scipara_getspeed_of_sound__", None, builtin_scipara_getspeed_of_sound)),
            ('__intern_scipara_getknot__', VariableType.Function, BuiltinFunction("__intern_scipara_getknot__", None, builtin_scipara_getknot)),
            ('__intern_scipara_getzero_Celsius__', VariableType.Function, BuiltinFunction("__intern_scipara_getzero_Celsius__", None, builtin_scipara_getzero_Celsius)),
            ('__intern_scipara_getdegree_Fahrenheit__', VariableType.Function, BuiltinFunction("__intern_scipara_getdegree_Fahrenheit__", None, builtin_scipara_getdegree_Fahrenheit)),
            ('__intern_scipara_geteV__', VariableType.Function, BuiltinFunction("__intern_scipara_geteV__", None, builtin_scipara_geteV)),
            ('__intern_scipara_getelectron_volt__', VariableType.Function, BuiltinFunction("__intern_scipara_getelectron_volt__", None, builtin_scipara_getelectron_volt)),
            ('__intern_scipara_getcalorie__', VariableType.Function, BuiltinFunction("__intern_scipara_getcalorie__", None, builtin_scipara_getcalorie)),
            ('__intern_scipara_getcalorie_th__', VariableType.Function, BuiltinFunction("__intern_scipara_getcalorie_th__", None, builtin_scipara_getcalorie_th)),
            ('__intern_scipara_getcalorie_IT__', VariableType.Function, BuiltinFunction("__intern_scipara_getcalorie_IT__", None, builtin_scipara_getcalorie_IT)),
            ('__intern_scipara_geterg__', VariableType.Function, BuiltinFunction("__intern_scipara_geterg__", None, builtin_scipara_geterg)),
            ('__intern_scipara_getBtu__', VariableType.Function, BuiltinFunction("__intern_scipara_getBtu__", None, builtin_scipara_getBtu)),
            ('__intern_scipara_getBtu_IT__', VariableType.Function, BuiltinFunction("__intern_scipara_getBtu_IT__", None, builtin_scipara_getBtu_IT)),
            ('__intern_scipara_getBtu_th__', VariableType.Function, BuiltinFunction("__intern_scipara_getBtu_th__", None, builtin_scipara_getBtu_th)),
            ('__intern_scipara_getton_TNT__', VariableType.Function, BuiltinFunction("__intern_scipara_getton_TNT__", None, builtin_scipara_getton_TNT)),
            ('__intern_scipara_gethp__', VariableType.Function, BuiltinFunction("__intern_scipara_gethp__", None, builtin_scipara_gethp)),
            ('__intern_scipara_gethorsepower__', VariableType.Function, BuiltinFunction("__intern_scipara_gethorsepower__", None, builtin_scipara_gethorsepower)),
            ('__intern_scipara_getdyn__', VariableType.Function, BuiltinFunction("__intern_scipara_getdyn__", None, builtin_scipara_getdyn)),
            ('__intern_scipara_getdyne__', VariableType.Function, BuiltinFunction("__intern_scipara_getdyne__", None, builtin_scipara_getdyne)),
            ('__intern_scipara_getlbf__', VariableType.Function, BuiltinFunction("__intern_scipara_getlbf__", None, builtin_scipara_getlbf)),
            ('__intern_scipara_getpound_force__', VariableType.Function, BuiltinFunction("__intern_scipara_getpound_force__", None, builtin_scipara_getpound_force)),
            ('__intern_scipara_getkgf__', VariableType.Function, BuiltinFunction("__intern_scipara_getkgf__", None, builtin_scipara_getkgf)),
            ('__intern_scipara_getkilogram_force__', VariableType.Function, BuiltinFunction("__intern_scipara_getkilogram_force__", None, builtin_scipara_getkilogram_force)),

            ('__intern_scipara_getversion__', VariableType.Function, BuiltinFunction("__intern_scipara_getversion__", None, builtin_scipara_getversion)),

						('__intern_os_args__', VariableType.Function, BuiltinFunction("__intern_os_args__", None, builtin_os_args)),

            ('__intern_clear__', VariableType.Function, BuiltinFunction("__intern_clear__", None, builtin_clear)),
            ('__intern_quit__', VariableType.Function, BuiltinFunction("__intern_quit__", None, builtin_quit)),
            ('__intern_exit__', VariableType.Function, BuiltinFunction("__intern_exit__", None, builtin_exit)),

            ('__intern_int_add__', VariableType.Function, BuiltinFunction("__intern_int_add__", None, builtin_int_add)),
            ('__intern_int_sub__', VariableType.Function, BuiltinFunction("__intern_int_sub__", None, builtin_int_sub)),
            ('__intern_int_mul__', VariableType.Function, BuiltinFunction("__intern_int_mul__", None, builtin_int_mul)),
            ('__intern_int_div__', VariableType.Function, BuiltinFunction("__intern_int_div__", None, builtin_int_div)),
            ('__intern_int_mod__', VariableType.Function, BuiltinFunction("__intern_int_mod__", None, builtin_int_mod)),
            ('__intern_int_bitor__', VariableType.Function, BuiltinFunction("__intern_int_bitor__", None, builtin_int_bitor)),
            ('__intern_int_bitand__', VariableType.Function, BuiltinFunction("__intern_int_bitand__", None, builtin_int_bitand)),
            ('__intern_int_bitxor__', VariableType.Function, BuiltinFunction("__intern_int_bitxor__", None, builtin_int_bitxor)),

            ('__intern_float_add__', VariableType.Function, BuiltinFunction("__intern_float_add__", None, builtin_float_add)),
            ('__intern_float_sub__', VariableType.Function, BuiltinFunction("__intern_float_sub__", None, builtin_float_sub)),
            ('__intern_float_mul__', VariableType.Function, BuiltinFunction("__intern_float_mul__", None, builtin_float_mul)),
            ('__intern_float_div__', VariableType.Function, BuiltinFunction("__intern_float_div__", None, builtin_float_div)),
            ('__intern_float_mod__', VariableType.Function, BuiltinFunction("__intern_float_mod__", None, builtin_float_mod)),

            ('__intern_time_sleep__', VariableType.Function, BuiltinFunction("__intern_time_sleep__", None, builtin_time_sleep)),
            ('__intern_time_now__',   VariableType.Function, BuiltinFunction("__intern_time_now__", None, builtin_time_now)),

            ('__intern_macro_expand__', VariableType.Function, BuiltinFunction("__intern_macro_expand__", None, builtin_macro_expand))
        ]

    def vartype_to_typeobject(self, vartype):
        if vartype == VariableType.Function:
            return self.func_type
        elif vartype == VariableType.Type:
            return self.basic_type
        elif vartype == VariableType.Object:
            return self.basic_object

        raise Exception('No conversion defined for {}'.format(vartype))

    def apply_to_scope(self, scope):
        for (name, vtype, value) in self.variables:
            var_type = vtype

            type_object = self.vartype_to_typeobject(var_type)

            scope.declare_variable(name, type_object)

            var = scope.find_variable_value(name)
            var.assign_value(value)
