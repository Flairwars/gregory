from discord.ext import commands
from discord import errors
import discord
from discord.ext import commands
import aiohttp
import numpy as np
import math
import matplotlib.pyplot as plt


# TODO: check for redundant imports

class quadfunc(commands.Cog, name='math'):
    '''
    Quadratic equation solver
    Made by u/SomebodyNotFamous

    Note:Im from Poland and this code was originaly written in Polish. I've tried to translate my code (and the messages the bot sends)
    into english, howere there still may be some mistakes. If you notice any problems with the translations please let me know and I will
    fix them ASAP. Note2:Because you cant just do " DELTA = B^2 - 4 * A * C " (or maybe you can and my brain is just smooth) i split
    equations like these into smaller parts. For a example of this look at line 18.
    '''

    def __init__(self, client):
        self.client = client

    def obliczenia(A, B, C):  # "obliczenia" means calculations in Polish
        # DELTA = math.pow(B, 2) - 4 * A * C <- this doesnt work so i split it into 3 simpler operations below (CZ1D - CZ3D)
        CZ1D = math.pow(float(B), 2)
        CZ2D = float(A) * float(C)
        CZ3D = 4 * CZ2D
        DELTA = CZ1D - CZ3D
        return DELTA

    # I believe i could rewrite the above code to include it in the function below, however tis also works fine

    def cozdelta(DELTA, A, B, C):  # "cozdelta" (or rather "co z deltą?"") can be somewhat translated to: What do we do with the delta?
        delta_status = "unless you are browsing Github, you should not be able to see this text. If you do see this on discord, " \
                       "notify u/SomebodyNotFamous on Megaserver. "
        if (DELTA < 0):
            # wierzchołek x
            P1APEX = (-float(B))
            P2APEX = 2 * float(A)
            try:
                APEXX = P1APEX / P2APEX
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            # wierzchołek y
            NEGATIVEDELTA = 0 - DELTA
            P2APEXY = 4 * float(A)
            try:
                APEXY = NEGATIVEDELTA / P2APEXY
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status

            if (A < 0):
                delta_status = "There are no roots, the entire graph is below the x axis." + str(
                    APEXY) + " is the maxvalue of the function for X = " + str(APEXX) + " ."
                return delta_status
            if (A > 0):
                delta_status = "There are no roots for this function. The entire graph is above the X axis and the max value of the " \
                               "fuction cannot be found "
                return delta_status
        if (DELTA == 0):
            # wierzchołek x
            P1APEX = (-float(B))
            P2APEX = 2 * float(A)
            try:
                APEXX = P1APEX / P2APEX
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            # wierzchołek y
            NEGATIVEDELTA = 0 - DELTA
            P2APEXY = 4 * float(A)
            try:
                APEXY = NEGATIVEDELTA / P2APEXY
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            if (A < 0):
                delta_status = "The root of the fuction is " + str(APEXX) + " . The max value of the function is Y = " + str(APEXY) + " ."
                return delta_status
            if (A > 0):
                delta_status = "The root of the function is" + str(APEXX) + ", it is imposiible to get the max value of this function."
                return delta_status
        if (DELTA > 0):
            # wierzchołek x
            P1APEX = (-float(B))
            P2APEX = 2 * float(A)
            try:
                APEXX = P1APEX / P2APEX
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            # wierzchołek y
            NEGATIVEDELTA = 0 - DELTA
            P2APEXY = 4 * float(A)
            try:
                APEXY = NEGATIVEDELTA / P2APEXY
            except ZeroDivisionError:
                delta_status = "Error: You attempted to divide by zero"
                return delta_status
            # X1 i X2
            A2 = 2 * float(A)
            MINUSB = (-float(B))
            SQRTDELTA = math.sqrt(DELTA)
            X1P1 = MINUSB + SQRTDELTA
            X2P1 = MINUSB - SQRTDELTA
            X1 = X1P1 / A2
            X2 = X2P1 / A2
            Y1 = float(A) * X1 ** 2 + float(B) * X1 + float(C)
            Y2 = float(A) * X2 ** 2 + float(B) * X2 + float(C)
            if (A < 0):
                delta_status = "The roots of this fuction are: X1= " + str(X1) + " for Y= " + str(Y2) + " and X2= " + str(
                    X2) + " for Y= " + str(Y2) + " . The max value of this function is Y= " + str(APEXY) + " for X= " + str(APEXX) + " ."
                return delta_status
            if (A > 0):
                delta_status = "The roots of this fuction are: X1= " + str(X1) + " for Y= " + str(Y2) + " and X2= " + str(
                    X2) + " for Y= " + str(
                    Y2) + " . It is the imposiible to get this functions max value. The apex of this function Y= " + str(
                    APEXY) + " for X= " + str(APEXX) + " ."
                return delta_status

    @commands.command(aliases=['quadfunc'])
    async def qff(self, ctx, arg1, arg2, arg3):
        wrong_values = False  # i create a self explenatory(<-- i hope i typed this right lol) variable
        try:  # we try to convert the argguments from strings to floatr type. This is needed for the calculations.
            try:  # we try to convert A into a float and create strA for later use
                A = float(arg1)
                strA = str(A)
            except IndexError:  # if the conversion results in a error (ie. someone included a invalid argument when trying to use this
                # solver)
                await ctx.send("Incorrect argument A")  # we tell the user which one of the inputed arguments was incorrect
            try:  # same as above but for B
                B = float(arg2)
                strB = str(B)
            except IndexError:
                await ctx.send("Incorrect argument B")
            try:  # and we do this again, but this time for C
                C = float(arg3)
                strC = str(C)
            except IndexError:
                await ctx.send("Incorrect argument C")
        except ValueError:  # If one of the above convertions returns a error we...
            await ctx.send("Value Error")  # ...tell the user about it...
            wrong_values = True  # ...and tell the program about it

        if (wrong_values):  # Input was incorrect so we dont solve anything
            await ctx.send("Your input was incorrect.")  # we tell the user about this
        else:  # else we do the solving
            await ctx.send("A: " + strA + "\n" + "B: " + strB + "\n" + "C: " + strC + "\n" + "Delta: " + str(
                quadfunc.obliczenia(A, B, C)) + '\n' + str(quadfunc.cozdelta(quadfunc.obliczenia(A, B, C), A, B, C)))
            # we send the   |---------------------Arguments used-------------------| |----------------delta value----------------------|
            # |------------------the solved function------------------------|


def setup(client):
    client.add_cog(quadfunc(client))
