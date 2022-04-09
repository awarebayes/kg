#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define MAX(a,b) (((a)>(b))?(a):(b))
#define MIN(a,b) (((a)<(b))?(a):(b))

int signi(int val)
{
	if (val > 0)
		return 1;
	else if (val == 0)
		return 0;
	else
		return -1;
}

void place_pixel(int x, int y)
{
	return;
}


void place_pixeli(int x, int y, int intensity)
{
	return;
}

void dda(int x_1, int y_1, int x_2, int y_2)
{
    int length = MAX(abs(x_2 - x_1), abs(y_2 - y_1));

	double dx = (x_2 - x_1) / length;
	double dy = (y_2 - y_1) / length;

	double x = x_1;
	double y = y_1;
	for (int i = 0; i < length; i++)
		place_pixel(round(x), round(y));
		x += dx;
		y += dy;
}

void bresenhem_float(int x_1, int y_1, int x_2, int y_2)
{
	double dx = abs(x_2 - x_1);
	double dy = abs(y_2 - y_1);

	double sign_dx = copysign(1, x_2 - x_1);
	double sign_dy = copysign(1, y_2 - y_1);

	int exchanged = 0;
	if(dy > dx)
	{

		double temp_dy = dy;
		dy = dx;
		dx = temp_dy;
		exchanged = 1;
	}

	double error = dy / dx - 0.5;
	double x = x_1;
	double y = y_1;
	double tan = dy / dx;

	for (int i = 0; i < dx; i++)
	{
		place_pixel(x, y);
		if (error >= 0)
		{
			if (exchanged)
				x += sign_dx;
			else
				y += sign_dy;
			error -= 1;
		}
		if (error <= 0)
		{
			if (exchanged)
				y += sign_dy;
			else
				x += sign_dx;
			error += dy / dx;
		}
	}
}


void bresenhem_int(int x_1, int y_1, int x_2, int y_2)
{
	int dx = abs(x_2 - x_1);
	int dy = abs(y_2 - y_1);

	int sign_dx = signi(x_2 - x_1);
	int sign_dy = signi(y_2 - y_1);

	int exchanged = 0;
	if(dy > dx)
	{

		int temp_dy = dy;
		dy = dx;
		dx = temp_dy;
		exchanged = 1;
	}

	int error = 2 * dy - dx;
	int x = x_1;
	int y = y_1;

	for (int i = 0; i < dx; i++)
	{
		place_pixel(x, y);
		if (error >= 0)
		{
			if (exchanged)
				x += sign_dx;
			else
				y += sign_dy;
			error -=  2 * dx;
		}
		else
		{
			if (exchanged)
				y += sign_dy;
			else
				x += sign_dx;
			error += 2 * dy;
		}
	}
}


void bresenhem_smooth(int x_1, int y_1, int x_2, int y_2)
{
	double I = 255;
	double dx = abs(x_2 - x_1);
	double dy = abs(y_2 - y_1);

	double sign_dx = copysign(1, x_2 - x_1);
	double sign_dy = copysign(1, y_2 - y_1);

	int exchanged = 0;
	if(dy > dx)
	{

		double temp_dy = dy;
		dy = dx;
		dx = temp_dy;
		exchanged = 1;
	}

	double tan = dy / dx * I;
	double error = I / 2;
	double W = I - tan;

	double x = x_1;
	double y = y_1;

	for (int i = 0; i < dx; i++)
	{
		place_pixel(x, y);
		if (error < W)
		{
			if (exchanged)
				y += sign_dy;
			else
				x += sign_dx;
			error += tan;
		}
		else
		{
			y += sign_dy;
			x += sign_dx;
			error -= W;
		}
	}
}


void wu_x_line(int x_1, int y_1, int x_2, int y_2)
{
	double I = 255;
	double dx = (x_2 - x_1);
	double dy = (y_2 - y_1);

	double tan = dx / dy;

	if (y_1 > y_2)
	{
		tan *= -1;
	}

	double x = x_1;
	for (int y = y_1; y < y_2; y+= 1)
	{
		double d_1 = x - floor(x);
		double d_2 = 1 - d_1;

		x += tan;
		int int_1 = round(fabs(d_1) * I);
		int int_2 = round(fabs(d_2) * I);
		place_pixeli( (int)floor(x), y, int_1);
		place_pixeli((int)floor(x)+1, y, int_2);
	}
}

void wu_y_line(int x_1, int y_1, int x_2, int y_2)
{
	double I = 255;
	double dx = (x_2 - x_1);
	double dy = (y_2 - y_1);

	double tan = dy / dx;

	if (y_1 > y_2)
	{
		tan *= -1;
	}

	double y = y_1;
	for (int x = x_1; x < x_2; x+= 1)
	{
		double d_1 = y - floor(y);
		double d_2 = 1 - d_1;

		x += tan;
		int int_1 = round(fabs(d_1) * I);
		int int_2 = round(fabs(d_2) * I);
		place_pixeli( x, floor(y), int_1);
		place_pixeli(x+1, floor(y), int_2);
	}
}

void wu(int x_1, int y_1, int x_2, int y_2)
{
	double dx = (x_2 - x_1);
	double dy = (y_2 - y_1);

	if (dx == 0)
	{
		for (int y = MIN(y_1, y_2); y < MAX(y_1, y_2); y++)
			place_pixel(x_1, y);
	}


	else if (dy == 0)
	{
		for (int x = MIN(x_1, x_2); x < MAX(x_1, x_2); x++)
			place_pixel(x, y_1);
	}

	else if (dy >= dx)
		wu_x_line(x_1, y_1, x_2, y_2);
	else
		wu_y_line(x_1, y_1, x_2, y_2);
}

double benchmark(void draw_func(int, int, int, int))
{
	double time = 0;
	long calls = 0;
	for (int deg = 0; deg < 360; deg++)
	{
		double radians = deg * M_PI / 180;
		int end_x = (int)(cos(radians) * 300);
		int end_y = (int)(sin(radians) * 300);
		for (int i = 0; i < 1000; i++)
		{
			clock_t start = clock();
			draw_func(0, 0, end_x, end_y);
			clock_t end = clock();

			clock_t elapsed = end - start;
			double time_taken = ((double) elapsed) / CLOCKS_PER_SEC * 1000000;
			time += time_taken;
			calls += 1;
		}
	}
	return time / calls;
}

int main()
{
    benchmark(dda);
	printf("dda %f\n", benchmark(dda));
	printf("bresenhem_float %f\n", benchmark(bresenhem_float));
	printf("bresenhem_int %f\n", benchmark(bresenhem_int));
	printf("bresenhem_smooth %f\n", benchmark(bresenhem_smooth));
	printf("wu %f\n", benchmark(wu));
	return 0;
}