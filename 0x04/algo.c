#include <stdio.h>
#include <string.h>

int main()
{
  char buf[64];
  gets(buf);
  int l = strlen(buf);
  if (l * l != 144)
    return 1;
  unsigned int a = buf[0] | (buf[4] << 8) | (buf[8] << 16);
  unsigned int b = buf[1] | (buf[5] << 8) | (buf[9] << 16);
  unsigned int c = buf[2] | (buf[6] << 8) | (buf[10] << 16);
  unsigned int d = buf[3] | (buf[7] << 8) | (buf[11] << 16);
  if (!(((a % 3571) == 2963) && (((a % 2843) == 215)) && (((a % 30243) == 13059))))
    return 2;
  if (!(((b % 80735) == 51964) && (((b % 8681) == 2552)) && (((b % 40624) == 30931))))
    return 3;
  if (!(((c % 99892) == 92228) && (((c % 45629) == 1080)) && (((c % 24497) == 12651))))
    return 4;
  if (!(((d % 54750) == 26981) && (((d % 99627) == 79040)) && (((d % 84339) == 77510))))
    return 5;
  printf("Congratulations %s is flag\n", buf);
  return 0;
}
