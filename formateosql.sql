   
CREATE PROCEDURE [dbo].[UP_PROCESAR]    
@SELECCIONAR BIT = 0    
    
AS    
    
DECLARE @ZONASOC varchaR(3)     
DECLARE @ZONA VARCHAR(3)    
DECLARE @ANIO_CAMPANIA VARCHAR(6)    
DECLARE @PedidoID INT    
DECLARE @pPeriodoFiscal varchar(6)  = (SELECT PERIODO FROM objetivos WHERE convert(date, Getdate()) BETWEEN VigenciaDESDE and VigenciaHASTA)    
DECLARE @ZONAECO varchar(3) = (SELECT ZONAECO FROM PARAMETROS_SEGURIDAD)     
DECLARE @ID INT    
DECLARE @MONEDA varchar(10) = (SELECT top 1 MONEDA FROM PARAMETROS_SEGURIDAD)    
DECLARE @ZONAANDREANI varchar(3) = (SELECT ZONAANDREANI FROM PARAMETROS_SEGURIDAD)     

DECLARE db_cursor_PROC CURSOR FOR     
SELECT PedidoID FROM PEDIDOS_CAB_SAP WHERE (Zona = @ZONAECO OR Zona = @ZONAANDREANI) AND FPROCESO is NULL    
    
BEGIN TRY    
 BEGIN TRANSACTION;    
    
  OPEN db_cursor_PROC      
  FETCH NEXT FROM db_cursor_PROC INTO @PedidoID    
  WHILE @@FETCH_STATUS = 0      
  BEGIN    
    
   INSERT INTO PEDIDOS_CAB_TANGO (PEDIDOID,ZONA,SECCION,CLIENTE_NUMERO,COD_RAMO,ANIO,CAMPANIA,CANTIDAD_CAJAS,FECHA_FACTURA,    
    REMITO_NUMERO,IMPORTE_TOTAL,IMPORTE_IVA1,IMPORTE_IVA2,NUMERO_CBTE_SAP,PROVINCIA, CATEGORIA_IVA,IMPORTE_BONIFICADO1,    
    IMPORTE_BONIFICADO5,GASTOS_ADMINISTRATIVOS,EXCENTOS, Procesado, FALTA, Periodo)    
   SELECT PEDIDOID,ZONA,SECCION,CLIENTE_CODIGO,COD_RAMO,ANIO,CAMPANIA,CANTIDAD_CAJAS,FECHA_FACTURA,REMITO_NUMERO,IMPORTE_TOTAL,IMPORTE_IVA1,    
    IMPORTE_IVA2,NUMERO_CBTE_SAP,PROV_CODI,CATEGORIA_IVA,IMPORTE_BONIFICADO1,IMPORTE_BONIFICADO5,GASTOS_ADMINISTRATIVOS,EXCENTOS ,     
    1 , getdate(), @pPeriodoFiscal    
     FROM PEDIDOS_CAB_SAP     
    WHERE PEDIDOID = @PEDIDOID    
      
   SET @ID = (SELECT @@IDENTITY)    
      
   INSERT INTO PEDIDOS_DET_TANGO (PEDIDOS_CABID,PEDIDOID,DIGITO_VERIFICADOR,CODIGO_PRODUCTO,DIGITO_VERIFICADOR_PRODUCTO,TIPO_PRODUCTO,    
    ANIOCAMPANIA,CANTIDAD,IMPORTE_IVA2,PRECIO_NOTA_PEDIDO,IMPORTE_IVA1,DESCRIPCION,TIPOIMPUESTO,BONIFICACION,MONTIB,TIPPROD,RUBROID,     
    CODIGO_PRODUCTO_ORIGINAL)    
   SELECT @ID, TMP.PEDIDOID,TMP.DIGITO_VERIFICADOR,TMP.CODIGO_PRODUCTO,TMP.DIGITO_VERIFICADOR_PRODUCTO,TMP.TIPO_PRODUCTO,TMP.ANIOCAMPANIA,    
    TMP.CANTIDAD,TMP.IMPORTE_IVA2,TMP.PRECIO_NOTA_PEDIDO,TMP.IMPORTE_IVA1,TMP.DESCRIPCION,TMP.TIPOIMPUESTO,TMP.BONIFICACION,TMP.MONTIB,    
    TMP.TIPPROD, ISNULL( R.RubroID , 0)RubroID ,TMP.CODIGO_PRODUCTO    
     FROM PEDIDOS_DET_SAP TMP    
     LEFT JOIN PRODUCTOS PR    
      on TMP.Codigo_Producto = PR.Codigo_Producto    
     LEFT join Rubro_Grupo_Tipo RGT    
      on TMP.TIPPROD = RGT.GRUPO AND TMP.TIPO_PRODUCTO = RGT.TIPO    
     LEFT JOIN RUBROS R    
      on RGT.RUBROID = R.RUBROID    
    WHERE PEDIDOID = @PEDIDOID    
      AND TMP.CODIGO_PRODUCTO <> '100'    
      AND( isnull(TMP.CODIGO_PRODUCTO_KIT, '') = ''   OR isnull(TMP.CODIGO_PRODUCTO_KIT, '0') = '0' AND TMP.Precio_Nota_Pedido > 0     )  
       
    
   --EXEC UP_ACTUALIZAR_STOCK_ECOMMERCE_PEDIDOID @PedidoID    
      
   EXEC [UP_FICHA_PRODUCTO_INS_FIJA] @PEDIDOID     
    
   FETCH NEXT FROM db_cursor_PROC INTO @PedidoID    
  END     
    
  CLOSE db_cursor_PROC      
  DEALLOCATE db_cursor_PROC     
    
 COMMIT TRANSACTION;    
END TRY    
BEGIN CATCH    
    IF @@TRANCOUNT > 0    
        ROLLBACK TRAN    
    
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE(), @ErrorSeverity INT = ERROR_SEVERITY(), @ErrorState INT = ERROR_STATE();    
    
    RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);    
END CATCH;    
    
-- INSERT PRODUCTOS QUE NO EXISTEN ECOMMERCE    
WITH cte     
  AS (SELECT TIPO_PRODUCTO, digito_verificador_producto, tipprod, descripcion, codigo_producto, precio_nota_pedido, ANIOCAMPANIA, rn = Row_number()    
        OVER (PARTITION BY Codigo_Producto ORDER BY Precio_Nota_Pedido desc)     
        FROM pedidos_det_SAP    
    WHERE PEDIDOID IN (SELECT PedidoID FROM PEDIDOS_CAB_SAP WHERE (Zona = @ZONAECO OR Zona = @ZONAANDREANI) AND FPROCESO is NULL)    
         AND CODIGO_PRODUCTO NOT IN (SELECT CODIGO_PRODUCTO FROM PRODUCTOS)    
         AND CODIGO_PRODUCTO <> '100')      
INSERT INTO PRODUCTOS(Tipo_Material, Digito_Verificador, Grupo, Descripcion, Codigo_producto, Prechoyn, Monedan, Aniocamp)    
SELECT TIPO_PRODUCTO, digito_verificador_producto, tipprod, descripcion, codigo_producto, precio_nota_pedido,  @MONEDA, ANIOCAMPANIA     
  FROM cte     
 WHERE rn = 1     
 -- INSERT PRODUCTOS QUE NO EXISTEN ECOMMERCE    
    
UPDATE PEDIDOS_CAB_SAP     
   SET FPROCESO = GETDATE()     
 WHERE (Zona = @ZONAECO  or Zona = @ZONAANDREANI)
   AND FPROCESO is NULL    
    
create table #TempZonas     
(    
 Zona varchar(3),    
 Anio_Campania char(6),    
 Fecha date    
)     
    
create table #Zonas     
(    
 Zona varchar(3) ,    
 Anio_Campania varchar(6)    
)    
     
INSERT INTO #TempZonas     
SELECT ZONA, (convert(varchar(4), Anio) + convert(varchar(6), CAMPANIA)) 'ANIO_CAMPANIA' , Fecha_Factura    
  FROM PEDIDOS_CAB_SAP    
 WHERE FPROCESO IS NULL    
   AND ZONA NOT IN (SELECT ZONA FROM ZONAS WHERE EXCLUIR = 1)    
   AND ZONA <> @ZONAECO and ZONA <> @ZONAANDREANI     
 GROUP BY ZONA, Anio, Campania, FECHA_FACTURA     
    
INSERT INTO #Zonas (ZONA, ANIO_CAMPANIA)    
SELECT C.ZONA,  C.ANIO_CAMPANIA    
  FROM CALENDARIO C      
 LEFT JOIN ZONAS ZPORC     
  ON C.ZONA = ZPORC.ZONA    
 WHERE C.FECHA >= (SELECT VigenciaDesde FROM Objetivos WHERE Periodo =@pPeriodoFiscal)     
   AND C.FECHA <= (SELECT VigenciaHasta FROM Objetivos WHERE Periodo =@pPeriodoFiscal)     
   AND isnull(ZPORC.EXCLUIR,0) = 0     
   AND NOT EXISTS (Select 1 from CALCULOS C2 where C.ZONA = C2.ZONA and C.ANIO_CAMPANIA = C2.ANIO_CAMPANIA  AND C2.Periodo = @PPeriodoFIscal)    
 order by C.Fecha    
    
INSERT INTO #Zonas (ZONA, ANIO_CAMPANIA)    
SELECT C.ZONA, C.Anio_Campania    
  FROM #TempZonas C       
 LEFT JOIN Calendario C2 on C.Zona = C2.Zona and C.Anio_Campania= C2.Anio_Campania    
--WHERE C2.Zona is null    
  order by C.Fecha    
    
CREATE TABLE #T_PROYECTADO (result numeric(18,2))    
    
DECLARE db_cursor_ZONAS CURSOR FOR     
SELECT ZONA, ANIO_CAMPANIA FROM #ZONAS     
    
DECLARE db_cursor_ZONAS2 CURSOR FOR     
SELECT ZONA, ANIO_CAMPANIA FROM #ZONAS     
      
OPEN db_cursor_ZONAS      
FETCH NEXT FROM db_cursor_ZONAS INTO @ZONA, @ANIO_CAMPANIA    
WHILE @@FETCH_STATUS = 0      
BEGIN    
--Si cuando baja un pedido, la zona no existe en la tabla de ZONAS, hay que darla de alta automáticamente en la tabla de     
--ZONAS (con los campos fija falso, excluir falso, fechabaja null).     
--Y hay que insertar un registro en la tabla ZONA_PROVINCIAS     
--con la provincia que más veces esté repetida para esa zona en los pedidos que bajaron del día. Ej, hay 10 pedidos para la zona 306     
--para la provincia de córdoba y 2 pedidos para esa zona con provincia San Luis. La provincia a asignar es Córdoba porque se repite más veces.     
    
 IF(SELECT COUNT(*) FROM ZONAS WHERE ZONA = @ZONA) = 0    
 BEGIN    
      
    
  declare @Provincia char(3) = (select tmp.PROV_CODI from     
  (select top 1 PROV_CODI , count(*) Cantidad from PEDIDOS_CAB_SAP    
  WHERE ZONA = @ZONA    
  group by zona, PROV_CODI     
  order by 2 desc) as tmp)    
  if(@Provincia is not null)    
  BEGIN    
   insert into zonas(zona, FECHABAJA, FIJA, EXCLUIR)    
   values(@ZONA, null, 0,0)    
    
   insert into ZONA_PROVINCIAS    
   values (@ZONA, @Provincia)    
  END    
 END    
 DELETE FROM #T_PROYECTADO    
 DELETE FROM ZONA_PROYECTADO WHERE ZONA = @ZONA    
 AND ANIO_CAMPANIA = @ANIO_CAMPANIA    
 INSERT #T_PROYECTADO (RESULT )    
 EXEC UP_REG_LINEAL @ZONA, @ANIO_CAMPANIA    
    
 --SELECT @ZONA, @ANIO_CAMPANIA, RESULT FROM #T_PROYECTADO    
  INSERT INTO ZONA_PROYECTADO    
 VALUES (@ZONA, @ANIO_CAMPANIA, (SELECT isnull(RESULT,0) FROM #T_PROYECTADO))    
    
     
 FETCH NEXT FROM db_cursor_ZONAS INTO  @ZONA, @ANIO_CAMPANIA    
    
END     
      
CLOSE db_cursor_ZONAS    
DEALLOCATE db_cursor_ZONAS    
    
if @SELECCIONAR = 1    
BEGIN    
      
    EXEC UP_CALCULAR     
    
 OPEN db_cursor_ZONAS2      
 FETCH NEXT FROM db_cursor_ZONAS2 INTO @ZONA, @ANIO_CAMPANIA    
 WHILE @@FETCH_STATUS = 0      
 BEGIN    
     
  exec UP_SELECCIONAR_PEDIDOS @ZONA, @ANIO_CAMPANIA    
    
  FETCH NEXT FROM db_cursor_ZONAS2 INTO  @ZONA, @ANIO_CAMPANIA    
    
 END   
 
 DELETE PEDIDOS_CAB_TANGO WHERE PEDIDOS_CABID IN (
	SELECT PEDIDOS_CABID FROM PEDIDOS_CAB_TANGO WHERE PEDIDOS_CABID NOT IN (
		SELECT PEDIDOS_CABID FROM PEDIDOS_DET_TANGO WHERE PRECIO_NOTA_PEDIDO > 0.01 
	) AND ZONA <> @ZONAECO
 )

 DELETE PEDIDOS_DET_TANGO WHERE PEDIDOS_CABID NOT IN (
	SELECT DISTINCT PEDIDOS_CABID FROM PEDIDOS_CAB_TANGO
 )
      
 CLOSE db_cursor_ZONAS2      
 DEALLOCATE db_cursor_ZONAS2     
    
END