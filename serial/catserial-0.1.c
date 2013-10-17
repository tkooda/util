/** tkooda : 2005-12-28 : catserial : v0.1 **/

/* http://devsec.org/software/misc/catserial-0.1.c */

/*
 *   catserial is a simple command line tool that reads data from a
 *   serial device and prints it on stdout.
 *
 *   An environment variable may be set to specify serial settings:
 *
 *     CATSERIAL_BAUD = {50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200,230400}
 *
 *   I use it to read NMEA-0183 sentances from a BU-353 GPS USB mouse with:
 *
 *     CATSERIAL_BAUD=4800 ./catserial /dev/ttyUSB0
 *
 *   - Thor Kooda
 *     2005-12-28
*/

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>

#define MAX_BUF 8192

int main(int argc, char **argv)
{
  char *progname = argv[0];
  char *devpath = argv[1];
  char *env_baud;
  int fd, baud, rc;
  struct termios origterm, t;
  ssize_t in, out;
  unsigned char buf[ MAX_BUF + 1 ];
  
  // check args..
  if (argc != 2) {
    fprintf(stderr,"Usage: %s <serial device>\n",progname);
    return 1;
  }
  
  // open tty device..
  if ( -1 == (fd = open(devpath, O_RDWR)) ) {
    fprintf(stderr,"Error: could not open() '%s'\n",devpath);
    return 1;
  }
  
  // set serial settings if desired..
  if (env_baud = getenv("CATSERIAL_BAUD")) {
    switch (atoi(env_baud)) {
    case 50: baud = B50; break;
    case 75: baud = B75; break;
    case 110: baud = B110; break;
    case 134: baud = B134; break;
    case 150: baud = B150; break;
    case 200: baud = B200; break;
    case 300: baud = B300; break;
    case 600: baud = B600; break;
    case 1200: baud = B1200; break;
    case 1800: baud = B1800; break;
    case 2400: baud = B2400; break;
    case 4800: baud = B4800; break;
    case 9600: baud = B9600; break;
    case 19200: baud = B19200; break;
    case 38400: baud = B38400; break;
    case 57600: baud = B57600; break;
    case 115200: baud = B115200; break;
    case 230400: baud = B230400; break;
    default:
      fprintf(stderr,"Error: invalid environment variable CATSERIAL_BAUD: '%s'\n",env_baud);
      close(fd);
      return 1;
    }
    
    // save origional tty attributes for restoring later..
    if ( -1 == (rc = tcgetattr(fd, &t)) ) {
      fprintf(stderr,"Error: tcgetattr() failed\n");
      close(fd);
      return 1;
    }
    origterm = t;
    
    // set tty to communicate at baud speed..
    cfsetospeed(&t, baud);
    cfsetispeed(&t, baud);
    
    // set to N/8/1, non-canonical mode, and no RTS/CTS handshaking
    t.c_iflag &= ~(BRKINT|ICRNL|IGNCR|INLCR|INPCK|ISTRIP|IXON|IXOFF|PARMRK);
    t.c_iflag |= IGNBRK|IGNPAR;
    t.c_oflag &= ~(OPOST);
    t.c_cflag &= ~(CRTSCTS|CSIZE|HUPCL|PARENB);
    t.c_cflag |= (CLOCAL|CS8|CREAD);
    t.c_lflag &= ~(ECHO|ECHOE|ECHOK|ECHONL|ICANON|IEXTEN|ISIG);
    t.c_cc[VMIN] = 0;
    t.c_cc[VTIME] = 3;
    
    if ( -1 == (rc = tcsetattr(fd, TCSAFLUSH, &t)) ) {
      fprintf(stderr,"Error: tcsetattr() failed\n");
      close(fd);
      return 1;
    }
    
  }
  
  if ( -1 == (rc = tcflush(fd, TCIOFLUSH)) ) {
    fprintf(stderr,"Error: tcflush() failed\n");
    close(fd);
    return 1;
  }
  
  for (;;) {
    // read from tty, write to STDOUT..
    while ( 0 < (in = read(fd, buf, MAX_BUF)) ) {
      if ( in != (out = write(STDOUT_FILENO, buf, in)) ) {
	fprintf(stderr,"Error: write(STDOUT) failed\n");
	break;
      }
    }
    if ( in != 0 ) {
      fprintf(stderr,"Error: read() failed on '%s'\n",devpath);
      close(fd);
      return 1;
    }
  }
  
  // never get here, but..
  if (env_baud) {
    // reset tty to origional state..
    if ( -1 == (rc = tcsetattr(fd, TCSAFLUSH, &origterm)) ) {
      fprintf(stderr,"Error: tcsetattr() failed\n");
      close(fd);
      return 1;
    }
  }
  
  close(fd);
  return 0;
}
