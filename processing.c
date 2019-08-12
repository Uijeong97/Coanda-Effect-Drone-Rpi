import processing.serial. *; 

Serial myPort; // Create object from Serial class 
String datline; 

// 자이로의 이전 값과 이번의 값을 혼합하는 비율 
// 이전 값은 사용하지 않고 이번 값만 사용 하는 경우 1.0로 설정 
final float ratio = 0.5; 

// 마지막 x 축과 y 축의 값 (초기 값은 0~1023의 중앙값) 
float xGyroValueLast = 0; 
float yGyroValueLast = 0; 
float zGyroValueLast = 0; 

float xGyroValue; 
float yGyroValue; 
float zGyroValue; 

float xGyroAngleValue = 0; 
float yGyroAngleValue = 0; 
float zGyroAngleValue = 0; 

void setup () { 
  size (800, 800, P3D); 
  frameRate (30); 
  noStroke (); 
  colorMode (RGB 1); 

// Serial Port
  myPort = new Serial (this, "/dev/tty.raspberrypi-SerialPort", 9600); 
} 

void draw () { 
  background (0.5); 

  pushMatrix (); 

  translate (width / 2, height / 2, -30); 
  
  if (myPort.available ()> 0) {// if data is available, 
    String datline = myPort.readString (); 
    int [] splitdata = int (datline.split ( "")); 
    
    println (datline); 
    
    xGyroValue = float (splitdata [1]) / 100; 
    yGyroValue = float (splitdata [2]) / 100; 
    zGyroValue = float (splitdata [3]) / 100; 
    
    println (xGyroValue); 
    println (yGyroValue); 
    println (zGyroValue); 

  // 이전 값과 이번의 값의 비율을 바꾸어 스무딩 
  // 이전 값의 비율을 크게하면 반반하게 대신에 변화가 느
  // 이번 값의 비율을 늘리면 노이즈를 줍기 쉬워지는 대신에 변화가 빨라지 
  float xGyroValueSmoothed = xGyroValue * ratio + xGyroValueLast * (1.0 - ratio); 
  float yGyroValueSmoothed = yGyroValue * ratio + yGyroValueLast * (1.0 - ratio ); 
  float zGyroValueSmoothed = zGyroValue * ratio + zGyroValueLast * (1.0 - ratio); 

  // 이전 값으로 스무딩 값을 세트 
  xGyroValueLast = xGyroValueSmoothed; 
  yGyroValueLast = yGyroValueSmoothed; 
  zGyroValueLast = zGyroValueSmoothed; 
  
  // 각속도를 적분하여 각도로 변환 
  xGyroAngleValue = xGyroAngleValue + xGyroValueSmoothed * 0.005; 
  yGyroAngleValue = yGyroAngleValue + yGyroValueSmoothed * 0.005; 
  zGyroAngleValue = zGyroAngleValue + zGyroValueSmoothed * 0.005; 
  
  println (xGyroAngleValue);
  println (yGyroAngleValue); 
  println (zGyroAngleValue); 
 
} 
 
   // 마우스 대신 가속도 센서의 값으로 제어 
  rotateX (xGyroAngleValue); 
  rotateY (zGyroAngleValue); 
  rotateZ (yGyroAngleValue); 

  scale (200); 

  beginShape (QUADS); 

  fill ( 0, 1, 1); 
  vertex (-1, 1, 1); 
  fill (1, 1, 1); 
  vertex (1, 1, 1); 
  fill (1, 0, 1); 
  vertex (1, -1 1); 
  fill (0, 0, 1); 
  vertex (-1, -1, 1); 

  fill (1, 1, 1); 
  vertex (1, 1, 1); 
  fill (1, 1, 0) ; 
  vertex (1, 1, -1); 
  fill (1, 0, 0); 
  vertex (1, -1, -1); 
  fill (1, 0, 1); 
  vertex (1, -1, 1); 

  fill (1, 1, 0);
  vertex (1, 1, -1); 
  fill (0, 1, 0); 
  vertex (-1, 1, -1); 
  fill (0, 0, 0); 
  vertex (-1, -1, -1) ; 
  fill (1, 0, 0); 
  vertex (1, -1, -1); 

  fill (0, 1, 0); 
  vertex (-1, 1, -1); 
  fill (0, 1, 1); 
  vertex (-1, 1, 1); 
  fill (0, 0, 1); 
  vertex (-1, -1, 1); 
  fill (0, 0, 0); 
  vertex (-1, -1, -1) ; 

  fill (0, 1, 0); 
  vertex (-1, 1, -1); 
  fill (1, 1, 0); 
  vertex (1, 1, -1); 
  fill (1, 1, 1); 
  vertex (1, 1, 1); 
  fill (0, 1, 1); 
  vertex (-1, 1, 1); 

  fill (0, 0, 0); 
  vertex (-1, -1, -1); 
  fill ( 1, 0, 0); 
  vertex (1, -1, -1);
  fill (1, 0, 1); 
  vertex (1, -1, 1); 
  fill (0, 0, 1); 
  vertex (-1, -1, 1); 

  endShape (); 
  popMatrix (); 
}
