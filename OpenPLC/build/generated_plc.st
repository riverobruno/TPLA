PROGRAM elnuestro
  VAR
    Fotorresistor AT %IW0 : UINT;
    Pot AT %IW1 : UINT;
    Sensor_inc AT %IX0.1 : BOOL;
    led_inc AT %QX0.1 : BOOL;
    altavoz AT %QX0.0 : BOOL;
    laser AT %QW1 : UINT;
  END_VAR
  VAR
    mitadpot : UINT := 32768;
    a_encender : UINT := 2050;
    umbral_fotorres : UINT := 700;
    Timer_inc : TP;
    ritmo_alarma_laser : TP;
    Timer_inc_2 : TOF;
    duracion_alarma_laser : TP;
    ritmo_alarma_laser_2 : TOF;
    _TMP_GE16_OUT : BOOL;
    _TMP_AND13_OUT : BOOL;
    _TMP_NOT25_OUT : BOOL;
    _TMP_AND26_OUT : BOOL;
    _TMP_GE8_OUT : BOOL;
    _TMP_GE11_OUT : BOOL;
    _TMP_AND12_OUT : BOOL;
    _TMP_NOT33_OUT : BOOL;
    _TMP_AND30_OUT : BOOL;
    _TMP_OR19_OUT : BOOL;
    _TMP_BOOL_TO_UINT37_OUT : UINT;
    _TMP_MUL23_OUT : UINT;
  END_VAR

  _TMP_GE16_OUT := GE(Pot, 2050);
  _TMP_AND13_OUT := AND(Sensor_inc, _TMP_GE16_OUT);
  Timer_inc_2(IN := Timer_inc.Q, PT := T#500ms);
  _TMP_NOT25_OUT := NOT(Timer_inc_2.Q);
  _TMP_AND26_OUT := AND(_TMP_AND13_OUT, _TMP_NOT25_OUT);
  Timer_inc(IN := _TMP_AND26_OUT, PT := T#500ms);
  _TMP_GE8_OUT := GE(Pot, 32768);
  _TMP_GE11_OUT := GE(Fotorresistor, 700);
  _TMP_AND12_OUT := AND(_TMP_GE8_OUT, _TMP_GE11_OUT);
  duracion_alarma_laser(IN := _TMP_AND12_OUT, PT := T#5000ms);
  ritmo_alarma_laser_2(IN := ritmo_alarma_laser.Q, PT := T#300ms);
  _TMP_NOT33_OUT := NOT(ritmo_alarma_laser_2.Q);
  _TMP_AND30_OUT := AND(duracion_alarma_laser.Q, _TMP_NOT33_OUT);
  ritmo_alarma_laser(IN := _TMP_AND30_OUT, PT := T#300ms);
  _TMP_OR19_OUT := OR(Timer_inc.Q, ritmo_alarma_laser.Q);
  altavoz := _TMP_OR19_OUT;
  _TMP_BOOL_TO_UINT37_OUT := BOOL_TO_UINT(_TMP_GE8_OUT);
  _TMP_MUL23_OUT := MUL(Pot, _TMP_BOOL_TO_UINT37_OUT);
  laser := _TMP_MUL23_OUT;
  led_inc := _TMP_AND13_OUT;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : elnuestro;
  END_RESOURCE
END_CONFIGURATION
