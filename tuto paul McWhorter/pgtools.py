class LinearConverter:
    ''' x1,y1 : 1er pt de la courbe (souvent x1=0 ou la valeur min à convertir, y1 la valeur min après conversion)
        x2,y2 : 2eme pt de la courbe (souvent x2 la valeur max à convertir et y2 la valeur max après conversion)
        ex: potentiomètre qui envoie une valeur X entre 250 et 65535 et on veut convertir ça dans une plage Y allant de 0 à 100,
            alors x1=250,x2=65535,y1=0,y2=100.
    '''
    def __init__(self, x1, x2, y1, y2, limit_y=True):
        # examples :
        # x1=250 ; x2=65535 # pot min and max values found when testing
        # y1=0   ; y2=100   # target min and max values to convert to
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.y_min = min(y1,y2)
        self.y_max = max(y1,y2)
        self.limit_y = limit_y
        #Y=aX+b
        self.a=(y2-y1)/(x2-x1) # pente (d'après 2 points)
        self.b=y1-(self.a*x1) # ordonnée à l'origine (d'après 1 point) => y1=a*x1+b => b=y1-a*x1

    def conv(self, X):
        Y = self.a * X + self.b
        if self.limit_y:
            if Y < self.y_min: Y=self.y_min
            if Y > self.y_max: Y=self.y_max
        return Y
    
class SState():
    '''classe de base à hériter pour chaque état d'une machine à état (cf répertoire "fsm machine à états" )'''
    _val:int=0
    def val(self) -> int:
        return self._val
    def __str__(self) -> str:
        return f"{self.__class__.__name__}#{self._val}"