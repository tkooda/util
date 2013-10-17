/** tkooda : 2005-03-17 : ttyio : v0.1 **/
/* http://devsec.org/software/misc/ttyio-0.1.c */
/*
 *   A simple command line tool to write data to a serial device,
 *   (from STDIN), then read data from it (to STDOUT).
 *
 *   I use it to read data from an ibuttonlink temperature sensor with:
 *   `echo -n D | ./ttyio /dev/ttyS0`
 *
*/

#include <fcntl.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h>

#define MAX_BUF 4096

int main(int argc, char **argv)
{
  int fd, rc;
  ssize_t in, out;
  struct termios origterm, t;
  unsigned char buf[ MAX_BUF + 1 ];
  
  if (argc != 2) {
    printf("Usage: %s <tty device>",argv[0]);
    return 1;
  }
  
  // open tty..
  if ( -1 == (fd = open( argv[1], O_RDWR )) ) {
    printf("Error: could not open() '%s'\n",argv[1]);
    return 1;
  }
  
  // save origional tty attributes for restoring later..
  if ( -1 == (rc = tcgetattr(fd, &t)) ) {
    printf("Error: tcgetattr() failed\n");
    close(fd);
    return 1;
  }
  origterm = t;
  
  // setup tty (9600/N/8/1, NOHANDSHAKE)
  cfsetospeed(&t, B9600);
  cfsetispeed(&t, B9600);
  
  // set to non-canonical mode, and no RTS/CTS handshaking 
  t.c_iflag &= ~(BRKINT|ICRNL|IGNCR|INLCR|INPCK|ISTRIP|IXON|IXOFF|PARMRK);
  t.c_iflag |= IGNBRK|IGNPAR;
  t.c_oflag &= ~(OPOST);
  t.c_cflag &= ~(CRTSCTS|CSIZE|HUPCL|PARENB);
  t.c_cflag |= (CLOCAL|CS8|CREAD);
  t.c_lflag &= ~(ECHO|ECHOE|ECHOK|ECHONL|ICANON|IEXTEN|ISIG);
  t.c_cc[VMIN] = 0;
  t.c_cc[VTIME] = 3;
  
  if ( -1 == (rc = tcsetattr(fd, TCSAFLUSH, &t)) ) {
    printf("Error: tcsetattr() failed\n");
    close(fd);
    return 1;
  }
  
  if ( -1 == (rc = tcflush(fd, TCIOFLUSH)) ) {
    printf("Error: tcflush() failed\n");
    close(fd);
    return 1;
  }
  
  // read from STDIN, write to tty..
  while ( 0 < (in = read(STDIN_FILENO, buf, MAX_BUF)) ) {
    if ( in != (out = write(fd, buf, in)) ) {
      printf("Error: write(%s) failed\n",argv[1]);
      break;
    }
  }
  if ( in != 0 ) {
    printf("Error: read(STDIN) failed\n");
    close(fd);
    return 1;
  }
  
  // read from tty, write to STDOUT..
  while ( 0 < (in = read(fd, buf, MAX_BUF)) ) {
    if ( in != (out = write(STDOUT_FILENO, buf, in)) ) {
      printf("Error: write(STDOUT) failed\n");
      break;
    }
  }
  if ( in != 0 ) {
    printf("Error: read(%s) failed\n",argv[1]);
    close(fd);
    return 1;
  }
  
  // reset tty to origional state..
  if ( -1 == (rc = tcsetattr(fd, TCSAFLUSH, &origterm)) ) {
    printf("Error: tcsetattr() failed\n");
    close(fd);
    return 1;
  }
  
  close(fd);
  return 0;
}
