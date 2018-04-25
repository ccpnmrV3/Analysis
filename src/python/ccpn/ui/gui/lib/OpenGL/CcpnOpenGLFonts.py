"""
Module Documentation here
"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = ""
__credits__ = ""
__licence__ = ("")
__reference__ = ("")
#=========================================================================================
# Last code modification:
#=========================================================================================
__modifiedBy__ = "$modifiedBy$"
__dateModified__ = "$dateModified$"
__version__ = "$Revision$"
#=========================================================================================
# Created:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
#=========================================================================================
# Start of code
#=========================================================================================

import sys, os
from imageio import imread
from PyQt5 import QtWidgets
import numpy as np
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLArrays import GLVertexArray, GLRENDERMODE_DRAW
try:
  from OpenGL import GL, GLU, GLUT
except ImportError:
  app = QtWidgets.QApplication(sys.argv)
  QtWidgets.QMessageBox.critical(None, "OpenGL hellogl",
          "PyOpenGL must be installed to run this example.")
  sys.exit(1)


GlyphXpos = 'Xpos'
GlyphYpos = 'Ypos'
GlyphWidth = 'Width'
GlyphHeight = 'Height'
GlyphXoffset = 'Xoffset'
GlyphYoffset = 'Yoffset'
GlyphOrigW = 'OrigW'
GlyphOrigH = 'OrigH'
GlyphKerns = 'Kerns'
GlyphTX0 = 'tx0'
GlyphTY0 = 'ty0'
GlyphTX1 = 'tx1'
GlyphTY1 = 'ty1'
GlyphPX0 = 'px0'
GlyphPY0 = 'py0'
GlyphPX1 = 'px1'
GlyphPY1 = 'py1'


class CcpnGLFont():
  def __init__(self, fileName=None, size=12, base=0, fontTransparency=None, activeTexture=0):
    self.fontName = None
    self.fontGlyph = [None] * 256
    self.base = base

    with open(fileName, 'r') as op:
      self.fontInfo = op.read().split('\n')

    # no checking yet
    self.fontFile = self.fontInfo[0].replace('textures: ', '')
    self.fontPNG = imread(os.path.join(os.path.dirname(fileName), self.fontFile))
    self.fontName = self.fontInfo[1].split()[0]
    self.fontSize = self.fontInfo[1].split()[1]
    self.width = 0
    self.height = 0
    self.activeTexture = GL.GL_TEXTURE0+activeTexture
    self.activeTextureNum = activeTexture
    self.fontTransparency = fontTransparency

    row = 2
    exitDims = False

    # texture sizes
    dx = 1.0 / float(self.fontPNG.shape[1])
    dy = 1.0 / float(self.fontPNG.shape[0])
    hdx = dx / 10.0
    hdy = dy / 10.0

    line = ''
    chrNum = 0

    while exitDims is False and row < len(self.fontInfo):
      line = self.fontInfo[row]
      # print (line)
      if line.startswith('kerning'):
        exitDims = True
      else:
        try:
          lineVals = [int(ll) for ll in line.split()]
          if len(lineVals) == 9:
            chrNum, a0, b0, c0, d0, e0, f0, g0, h0 = lineVals

            # only keep the simple chars for the minute
            if chrNum < 256:
              self.fontGlyph[chrNum] = {}
              self.fontGlyph[chrNum][GlyphXpos] = a0
              self.fontGlyph[chrNum][GlyphYpos] = b0
              self.fontGlyph[chrNum][GlyphWidth] = c0
              self.fontGlyph[chrNum][GlyphHeight] = d0
              self.fontGlyph[chrNum][GlyphXoffset] = e0
              self.fontGlyph[chrNum][GlyphYoffset] = f0
              self.fontGlyph[chrNum][GlyphOrigW]= g0
              self.fontGlyph[chrNum][GlyphOrigH] = h0
              self.fontGlyph[chrNum][GlyphKerns] = {}

              # TODO:ED okay for now, but need to check for rounding errors

              # calculate the coordinated within the texture
              x = a0#+0.5           # self.fontGlyph[chrNum][GlyphXpos])   # try +0.5 for centre of texel
              y = b0#-0.005           # self.fontGlyph[chrNum][GlyphYpos])
              px = e0           # self.fontGlyph[chrNum][GlyphXoffset]
              py = f0           # self.fontGlyph[chrNum][GlyphYoffset]
              w = c0#-1           # self.fontGlyph[chrNum][GlyphWidth]+1       # if 0.5 above, remove the +1
              h = d0+0.5           # self.fontGlyph[chrNum][GlyphHeight]+1
              gw = g0           # self.fontGlyph[chrNum][GlyphOrigW]
              gh = h0           # self.fontGlyph[chrNum][GlyphOrigH]

              # coordinates in the texture
              self.fontGlyph[chrNum][GlyphTX0] = x*dx
              self.fontGlyph[chrNum][GlyphTY0] = (y+h)*dy
              self.fontGlyph[chrNum][GlyphTX1] = (x+w)*dx
              self.fontGlyph[chrNum][GlyphTY1] = y*dy

              # coordinates mapped to the quad
              self.fontGlyph[chrNum][GlyphPX0] = px
              self.fontGlyph[chrNum][GlyphPY0] = gh-(py+h)
              self.fontGlyph[chrNum][GlyphPX1] = px+(w)
              self.fontGlyph[chrNum][GlyphPY1] = gh-py

              # draw the quad
              # GL.glTexCoord2f( tx0, ty0);         GL.glVertex(px0, py0)
              # GL.glTexCoord2f( tx0, ty1);         GL.glVertex(px0, py1)
              # GL.glTexCoord2f( tx1, ty1);         GL.glVertex(px1, py1)
              # GL.glTexCoord2f( tx1, ty0);         GL.glVertex(px1, py0)

              if chrNum == 65:
                # use 'A' for the referencing the tab size
                self.width = gw
                self.height = gh

          else:
            exitDims = True
        except:
          exitDims = True
      row += 1

    if line.startswith('kerning'):
      # kerning list is included

      exitKerns = False
      while exitKerns is False and row < len(self.fontInfo):
        line = self.fontInfo[row]
        # print(line)

        try:
          lineVals = [int(ll) for ll in line.split()]
          chrNum, chrNext, val = lineVals

          if chrNum < 256 and chrNext < 256:
            self.fontGlyph[chrNum][GlyphKerns][chrNext] = val
        except:
          exitKerns = True
        row += 1

    width, height, ascender, descender = 0, 0, 0, 0
    for c in range(0, 256):
      if chrNum < 256 and self.fontGlyph[chrNum]:
        width = max( width, self.fontGlyph[chrNum][GlyphOrigW] )
        height = max( height, self.fontGlyph[chrNum][GlyphOrigH] )

    self.textureId = GL.glGenTextures(1)
    # GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glActiveTexture(self.activeTexture)
    GL.glBindTexture( GL.GL_TEXTURE_2D, self.textureId )

    if fontTransparency:
      for fontI in self.fontPNG:
        for fontJ in fontI:
          fontJ[3] = int(fontJ[3] * fontTransparency)

    GL.glTexImage2D( GL.GL_TEXTURE_2D, 0, GL.GL_RGBA
                     , self.fontPNG.shape[1], self.fontPNG.shape[0]
                     , 0
                     , GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, self.fontPNG.data )

    # generate a MipMap to cope with smaller text (may not be needed soon)
    GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST )
    GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST )

    # the following 2 lines generate a multitexture mipmap - shouldn't need here
    # GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR )
    # GL.glGenerateMipmap( GL.GL_TEXTURE_2D )
    GL.glDisable(GL.GL_TEXTURE_2D)

    # create a list of GLdisplayLists to handle each character - deprecated, changing to VBOs
    self.base = GL.glGenLists(256)
    dx = 1.0 / float(self.fontPNG.shape[1])
    dy = 1.0 / float(self.fontPNG.shape[0])
    for i in range(256):
      if self.fontGlyph[i] or i == 10 or i == 9:    # newline and tab
        # c = chr(i)

        GL.glNewList(self.base + i, GL.GL_COMPILE)
        if (i == 10):                                 # newline
          GL.glPopMatrix()
          GL.glTranslatef(0.0, -height, 0.0)
          GL.glPushMatrix()
        elif (i == 9):                                # tab
          GL.glTranslatef(4.0 * width, 0.0, 0.0)
        elif (i >= 32):
          x = float(self.fontGlyph[i][GlyphXpos])   # try +0.5 for centre of texel
          y = float(self.fontGlyph[i][GlyphYpos])
          px = self.fontGlyph[i][GlyphXoffset]
          py = self.fontGlyph[i][GlyphYoffset]
          w = self.fontGlyph[i][GlyphWidth]+1       # if 0.5 above, remove the +1
          h = self.fontGlyph[i][GlyphHeight]+1
          gw = self.fontGlyph[i][GlyphOrigW]
          gh = self.fontGlyph[i][GlyphOrigH]

          GL.glBegin(GL.GL_QUADS)

          # coordinates in the texture
          tx0 = x*dx
          ty0 = (y+h)*dy
          tx1 = (x+w)*dx
          ty1 = y*dy
          # coordinates mapped to the quad
          px0 = px
          py0 = gh-(py+h)
          px1 = px+w
          py1 = gh-py

          # draw the quad
          GL.glTexCoord2f( tx0, ty0);         GL.glVertex(px0, py0)
          GL.glTexCoord2f( tx0, ty1);         GL.glVertex(px0, py1)
          GL.glTexCoord2f( tx1, ty1);         GL.glVertex(px1, py1)
          GL.glTexCoord2f( tx1, ty0);         GL.glVertex(px1, py0)

          GL.glEnd()
          GL.glTranslatef(gw, 0.0, 0.0)
        GL.glEndList()

  def get_kerning(self, fromChar, prevChar):
    if self.fontGlyph[ord(fromChar)]:
      if prevChar and ord(prevChar) in self.fontGlyph[ord(fromChar)][GlyphKerns]:
        return self.fontGlyph[ord(fromChar)][GlyphKerns][ord(prevChar)]

    return 0


class GLString(GLVertexArray):
  def __init__(self, text=None, font=None, obj=None, color=(1.0, 1.0, 1.0, 1.0),
               x=0.0, y=0.0,
               ox=0.0, oy=0.0,
               angle=0.0, width=None, height=None, GLContext=None):
    super(GLString, self).__init__(renderMode=GLRENDERMODE_DRAW, blendMode=True
                                   , GLContext=GLContext, drawMode=GL.GL_TRIANGLES
                                   , dimension=2)
    if text is None:
      text = ''

    self.text = text
    self.font = font
    self.object = obj
    self.pid = obj.pid if hasattr(obj, 'pid') else None
    self.vertices = np.zeros((len(text) * 4, 2), dtype=np.float32)
    self.indices = np.zeros((len(text) * 6,), dtype=np.uint)
    self.colors = np.zeros((len(text) * 4, 4), dtype=np.float32)
    self.texcoords = np.zeros((len(text) * 4, 2), dtype=np.float32)
    # self.attribs = np.zeros((len(text) * 4, 2), dtype=np.float32)
    # self.offsets = np.zeros((len(text) * 4, 2), dtype=np.float32)
    self.indexOffset = 0
    penX = penY = 0              # offset the string from (0,0) and use (x,y) in shader
    prev = None

    # cs, sn = math.cos(angle), math.sin(angle)
    # rotate = np.matrix([[cs, sn], [-sn, cs]])

    for i, charCode in enumerate(text):
      c = ord(charCode)
      glyph = font.fontGlyph[c]

      if glyph or c == 10 or c == 9:    # newline and tab

        if (c == 10):                                 # newline
          penX = 0
          penY = 0      #penY + font.height
          # for vt in self.vertices:
          #   vt[1] = vt[1] + font.height
          self.vertices[:, 1] += font.height

        elif (c == 9):                                # tab
          penX = penX + 4 * font.width

        elif (c >= 32):

          kerning = font.get_kerning(charCode, prev)

          # TODO:ED check that these are correct
          x0 = penX + glyph[GlyphPX0] + kerning     # penX + glyph.offset[0] + kerning
          y0 = penY + glyph[GlyphPY0]               # penY + glyph.offset[1]
          x1 = penX + glyph[GlyphPX1] + kerning     # x0 + glyph.size[0]
          y1 = penY + glyph[GlyphPY1]               # y0 - glyph.size[1]
          u0 = glyph[GlyphTX0]          # glyph.texcoords[0]
          v0 = glyph[GlyphTY0]          # glyph.texcoords[1]
          u1 = glyph[GlyphTX1]          # glyph.texcoords[2]
          v1 = glyph[GlyphTY1]          # glyph.texcoords[3]

          # # apply rotation to the text
          # xbl, ybl = x0 * cs + y0 * sn, -x0 * sn + y0 * cs
          # xtl, ytl = x0 * cs + y1 * sn, -x0 * sn + y1 * cs
          # xtr, ytr = x1 * cs + y1 * sn, -x1 * sn + y1 * cs
          # xbr, ybr = x1 * cs + y0 * sn, -x1 * sn + y0 * cs

          index = i * 4
          indices = [index, index + 1, index + 2, index, index + 2, index + 3]
          vertices = [x0, y0], [x0, y1], [x1, y1], [x1, y0]
          texcoords = [[u0, v0], [u0, v1], [u1, v1], [u1, v0]]
          colors = [color, ] * 4
          # attribs = [[x, y], [x, y], [x, y], [x, y]]
          # offsets = [[x, y], [x, y], [x, y], [x, y]]

          self.vertices[i * 4:i * 4 + 4] = vertices
          self.indices[i * 6:i * 6 + 6] = indices
          self.texcoords[i * 4:i * 4 + 4] = texcoords
          self.colors[i * 4:i * 4 + 4] = colors
          # self.attribs[i * 4:i * 4 + 4] = attribs
          # self.offsets[i * 4:i * 4 + 4] = offsets

          penX = penX + glyph[GlyphOrigW] + kerning
          # penY = penY + glyph[GlyphHeight]
          prev = charCode

      self.numVertices = len(self.vertices)
      self.attribs = np.array([x+ox, y+oy] * self.numVertices, dtype=np.float32)
      self.offsets = np.array([x, y] * self.numVertices, dtype=np.float32)
      self.lineWidths = [ox, oy]

    # total width of text - probably don't need
    # width = penX - glyph.advance[0] / 64.0 + glyph.size[0]

  def drawTextArray(self):
    # TODO:ED need to sort out the speed of this
    # GL.glActiveTexture(GL.GL_TEXTURE0)
    # GL.glBindTexture(GL.GL_TEXTURE_2D, self.font.textureId)

    self._GLContext.globalGL._shaderProgramTex.setGLUniform1i('texture', self.font.activeTextureNum)

    super(GLString, self).drawTextArray()

  def setColour(self, col):
    self.colors = np.array(col*self.numVertices, dtype=np.float32)

  def setStringOffset(self, attrib):
    self.attribs = self.offsets + np.array(attrib*self.numVertices, dtype=np.float32)