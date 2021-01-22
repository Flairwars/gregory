from discord.ext import commands
from discord import errors
import discord
from discord.ext import commands
import aiohttp, pathlib
import numpy as np
import math
import matplotlib.pyplot as plt

class quadfunc(commands.Cog, name='quadfunc'):
    '''
    Quadratic equation solver
    made by u/SomebodyNotFamous
    '''
    def obliczenia(A, B, C):
        #DELTA = math.pow(B, 2) - 4 * A * C
        CZ1D = math.pow(float(B), 2)
        CZ2D = float(A) * float(C)
        CZ3D = 4 * CZ2D
        DELTA = CZ1D - CZ3D
        return DELTA

    def cozdelta(DELTA, A, B, C):
        delta_status = "pog"
        if(DELTA < 0):
            #wierzchołek x
            P1WIERZCHOLEK = (-float(B))
            P2WIERZCHOLEK = 2 * float(A)
            try:
                WIERZCHOLEKX = P1WIERZCHOLEK/P2WIERZCHOLEK
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            #wierzchołek y
            NEGATIVEDELTA = 0 - DELTA 
            P2WIERZCHOLEKY = 4 * float(A)
            try:
                WIERZCHOLEKY = NEGATIVEDELTA/P2WIERZCHOLEKY
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            
            if(A < 0):
                delta_status = "There are no roots, the entire graph is below the x axis." + str(WIERZCHOLEKY) + " is the maxvalue of the function for X = " + str(WIERZCHOLEKX) + " ."
                return delta_status 
            if(A > 0):
                delta_status = "There are no roots for this function. The entire graph is above the X axis and the max value of the fuction cannot be found"
                return delta_status
        if(DELTA == 0):
            #wierzchołek x
            P1WIERZCHOLEK = (-float(B))
            P2WIERZCHOLEK = 2 * float(A)
            try:
                WIERZCHOLEKX = P1WIERZCHOLEK/P2WIERZCHOLEK
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            #wierzchołek y
            NEGATIVEDELTA = 0 - DELTA
            P2WIERZCHOLEKY = 4 * float(A)
            try:
                WIERZCHOLEKY = NEGATIVEDELTA/P2WIERZCHOLEKY
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            if(A < 0):
                delta_status = "The root of the fuction is " + str(WIERZCHOLEKX) + " . The max value of the function is Y = " + str(WIERZCHOLEKY) + " ."
                return delta_status
            if(A > 0):
                delta_status = "The root of the function is" + str(WIERZCHOLEKX) + ", it is imposiible to get the max value of this function."
                return delta_status
        if(DELTA > 0):
            #wierzchołek x
            P1WIERZCHOLEK = (-float(B))
            P2WIERZCHOLEK = 2 * float(A)
            try:
                WIERZCHOLEKX = P1WIERZCHOLEK/P2WIERZCHOLEK
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            #wierzchołek y
            NEGATIVEDELTA = 0 - DELTA
            P2WIERZCHOLEKY = 4 * float(A)
            try:
                WIERZCHOLEKY = NEGATIVEDELTA/P2WIERZCHOLEKY
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            #X1 i X2
            A2 = 2 * float(A)
            MINUSB = (-float(B))
            SQRTDELTA = math.sqrt(DELTA)
            X1P1 = MINUSB + SQRTDELTA
            X2P1 = MINUSB - SQRTDELTA
            X1 = X1P1/A2
            X2 = X2P1/A2
            Y1 = float(A)*X1**2 + float(B)*X1 + float(C)  
            Y2 = float(A)*X2**2 + float(B)*X2 + float(C)  
            if(A < 0):
                delta_status = "The roots of this fuction are: X1= " + str(X1) + " for Y= " + str(Y2) + " and X2= " + str(X2) + " for Y= " + str(Y2) + " . The max value of this function is Y= " + str(WIERZCHOLEKY) + " for X= " + str(WIERZCHOLEKX) + " ."
                return delta_status
            if(A > 0):
                delta_status = "The roots of this fuction are: X1= " + str(X1) + " for Y= " + str(Y2) + " and X2= " + str(X2) + " for Y= " + str(Y2) + " . It is the imposiible to get this functions max value. The apex of this function Y= " + str(WIERZCHOLEKY) + " for X= " + str(WIERZCHOLEKX) + " ."
                return delta_status

    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.command(aliases=['quadfunc'])
    async def qff(self, ctx, arg1, arg2, arg3):
        wrong_values = False
        try:
            try:
                A = float(arg1)
                strA = str(A)
            except IndexError:
                await ctx.send("Incorrect argument A")
            try:
                B = float(arg2)
                strB = str(B)
            except IndexError:
                await ctx.send("Incorrect argument B")
            try:
                C = float(arg3)
                strC = str(C)
            except IndexError:
                await ctx.send("Incorrect argument C")
        except ValueError:
            await ctx.send("Value Error")
            wrong_values = True
        if(wrong_values):
            await ctx.send("Your input was incorrect.")
        else:
            await ctx.send("A: " + strA +"\n"+"B: " + strB +"\n"+"C: " + strC +"\n"+"Delta: " + str(quadfunc.obliczenia(A, B, C)) +'\n' + str(quadfunc.cozdelta(quadfunc.obliczenia(A, B, C), A, B, C)))


def setup(client):
    client.add_cog(quadfunc(client))
