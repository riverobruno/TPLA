void LOGGER_init__(LOGGER *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->MSG,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->LEVEL,LOGLEVEL__INFO,retain)
  __INIT_VAR(data__->TRIG0,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void LOGGER_body__(LOGGER *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  if ((__GET_VAR(data__->TRIG,) && !(__GET_VAR(data__->TRIG0,)))) {
    #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
    #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)

   LogMessage(GetFbVar(LEVEL),(char*)GetFbVar(MSG, .body),GetFbVar(MSG, .len));
  
    #undef GetFbVar
    #undef SetFbVar
;
  };
  __SET_VAR(data__->,TRIG0,,__GET_VAR(data__->TRIG,));

  goto __end;

__end:
  return;
} // LOGGER_body__() 





void ELNUESTRO_init__(ELNUESTRO *data__, BOOL retain) {
  __INIT_LOCATED(UINT,__IW0,data__->FOTORRESISTOR,retain)
  __INIT_LOCATED_VALUE(data__->FOTORRESISTOR,0)
  __INIT_LOCATED(UINT,__IW1,data__->POT,retain)
  __INIT_LOCATED_VALUE(data__->POT,0)
  __INIT_LOCATED(BOOL,__IX0_1,data__->SENSOR_INC,retain)
  __INIT_LOCATED_VALUE(data__->SENSOR_INC,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_1,data__->LED_INC,retain)
  __INIT_LOCATED_VALUE(data__->LED_INC,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_0,data__->ALTAVOZ,retain)
  __INIT_LOCATED_VALUE(data__->ALTAVOZ,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(UINT,__QW1,data__->LASER,retain)
  __INIT_LOCATED_VALUE(data__->LASER,0)
  __INIT_VAR(data__->MITADPOT,32768,retain)
  __INIT_VAR(data__->A_ENCENDER,2050,retain)
  __INIT_VAR(data__->UMBRAL_FOTORRES,700,retain)
  TP_init__(&data__->TIMER_INC,retain);
  TP_init__(&data__->RITMO_ALARMA_LASER,retain);
  TOF_init__(&data__->TIMER_INC_2,retain);
  TP_init__(&data__->DURACION_ALARMA_LASER,retain);
  TOF_init__(&data__->RITMO_ALARMA_LASER_2,retain);
  __INIT_VAR(data__->_TMP_GE16_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_AND13_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_NOT25_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_AND26_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_GE8_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_GE11_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_AND12_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_NOT33_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_AND30_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_OR19_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_BOOL_TO_UINT37_OUT,0,retain)
  __INIT_VAR(data__->_TMP_MUL23_OUT,0,retain)
}

// Code part
void ELNUESTRO_body__(ELNUESTRO *data__) {
  // Initialise TEMP variables

  __SET_VAR(data__->,_TMP_GE16_OUT,,GE__BOOL__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (UINT)__GET_LOCATED(data__->POT,),
    (UINT)2050));
  __SET_VAR(data__->,_TMP_AND13_OUT,,AND__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_LOCATED(data__->SENSOR_INC,),
    (BOOL)__GET_VAR(data__->_TMP_GE16_OUT,)));
  __SET_VAR(data__->TIMER_INC_2.,IN,,__GET_VAR(data__->TIMER_INC.Q,));
  __SET_VAR(data__->TIMER_INC_2.,PT,,__time_to_timespec(1, 500, 0, 0, 0, 0));
  TOF_body__(&data__->TIMER_INC_2);
  __SET_VAR(data__->,_TMP_NOT25_OUT,,!(__GET_VAR(data__->TIMER_INC_2.Q,)));
  __SET_VAR(data__->,_TMP_AND26_OUT,,AND__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_VAR(data__->_TMP_AND13_OUT,),
    (BOOL)__GET_VAR(data__->_TMP_NOT25_OUT,)));
  __SET_VAR(data__->TIMER_INC.,IN,,__GET_VAR(data__->_TMP_AND26_OUT,));
  __SET_VAR(data__->TIMER_INC.,PT,,__time_to_timespec(1, 500, 0, 0, 0, 0));
  TP_body__(&data__->TIMER_INC);
  __SET_VAR(data__->,_TMP_GE8_OUT,,GE__BOOL__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (UINT)__GET_LOCATED(data__->POT,),
    (UINT)32768));
  __SET_VAR(data__->,_TMP_GE11_OUT,,GE__BOOL__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (UINT)__GET_LOCATED(data__->FOTORRESISTOR,),
    (UINT)700));
  __SET_VAR(data__->,_TMP_AND12_OUT,,AND__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_VAR(data__->_TMP_GE8_OUT,),
    (BOOL)__GET_VAR(data__->_TMP_GE11_OUT,)));
  __SET_VAR(data__->DURACION_ALARMA_LASER.,IN,,__GET_VAR(data__->_TMP_AND12_OUT,));
  __SET_VAR(data__->DURACION_ALARMA_LASER.,PT,,__time_to_timespec(1, 5000, 0, 0, 0, 0));
  TP_body__(&data__->DURACION_ALARMA_LASER);
  __SET_VAR(data__->RITMO_ALARMA_LASER_2.,IN,,__GET_VAR(data__->RITMO_ALARMA_LASER.Q,));
  __SET_VAR(data__->RITMO_ALARMA_LASER_2.,PT,,__time_to_timespec(1, 300, 0, 0, 0, 0));
  TOF_body__(&data__->RITMO_ALARMA_LASER_2);
  __SET_VAR(data__->,_TMP_NOT33_OUT,,!(__GET_VAR(data__->RITMO_ALARMA_LASER_2.Q,)));
  __SET_VAR(data__->,_TMP_AND30_OUT,,AND__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_VAR(data__->DURACION_ALARMA_LASER.Q,),
    (BOOL)__GET_VAR(data__->_TMP_NOT33_OUT,)));
  __SET_VAR(data__->RITMO_ALARMA_LASER.,IN,,__GET_VAR(data__->_TMP_AND30_OUT,));
  __SET_VAR(data__->RITMO_ALARMA_LASER.,PT,,__time_to_timespec(1, 300, 0, 0, 0, 0));
  TP_body__(&data__->RITMO_ALARMA_LASER);
  __SET_VAR(data__->,_TMP_OR19_OUT,,OR__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_VAR(data__->TIMER_INC.Q,),
    (BOOL)__GET_VAR(data__->RITMO_ALARMA_LASER.Q,)));
  __SET_LOCATED(data__->,ALTAVOZ,,__GET_VAR(data__->_TMP_OR19_OUT,));
  __SET_VAR(data__->,_TMP_BOOL_TO_UINT37_OUT,,BOOL_TO_UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (BOOL)__GET_VAR(data__->_TMP_GE8_OUT,)));
  __SET_VAR(data__->,_TMP_MUL23_OUT,,MUL__UINT__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (UINT)__GET_LOCATED(data__->POT,),
    (UINT)__GET_VAR(data__->_TMP_BOOL_TO_UINT37_OUT,)));
  __SET_LOCATED(data__->,LASER,,__GET_VAR(data__->_TMP_MUL23_OUT,));
  __SET_LOCATED(data__->,LED_INC,,__GET_VAR(data__->_TMP_AND13_OUT,));

  goto __end;

__end:
  return;
} // ELNUESTRO_body__() 





