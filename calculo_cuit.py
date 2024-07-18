def calcula_cuit(sexo, dni):
    # Convertir el número de sexo a cadena
    L = str(sexo)


    dni = str(dni).zfill(8)

    if len(dni) == 8:
        while True:
            cadena = L + dni

            suma = 0
            pond = 2

            for i in range(len(cadena) - 1, -1, -1):
                suma += int(cadena[i]) * pond
                
                pond += 1
                
                if pond == 8:
                    pond = 2

            mod_s = suma % 11
            vrf = 11 - mod_s

            if vrf >= 10 and L == "20" and vrf != 11:
                L = "23"
                continue
            elif vrf >= 10 and L == "27" and vrf != 11:
                L = "23"
                continue
            elif vrf >= 10 and L == "30" and vrf != 11:
                L = "33"
                continue
            elif vrf >= 10 and L == "33" and vrf != 11:
                L = "34"
                continue
            elif vrf == 11:
                vrf = 0

            return f"{L}-{dni}-{vrf}"

# Ejemplo de uso:
sexo = 20  # Hombre
dni = 18321667
resultado = calcula_cuit(sexo, dni)
print(resultado)
