SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


IF OBJECT_ID('dbo.VI_COMPENSA_MENSUAL', 'P') IS NOT NULL
	DROP PROC dbo.VI_COMPENSA_MENSUAL
GO
-- ====================================================================
-- Author	  :	OAB- MM
-- Create date: 2022-12-15
-- Description: Obtiene STOCK dia por dia	
-- Historial de Cambios:

-- Ejemplos:
-- EXEC VI_COMPENSA_MENSUAL '20220430'   -fecha contra la que evalua y con la que genera cortes (= arrastra hasta hoy los ajustes)
-- 
/*
	Debe crearse la tabla antes de compilar en la base

	CREATE TABLE [dbo].[GRUPOSACRUZAR](
		[ELGRUP] [char](4) NOT NULL,
		[SINEGOPOS] [char](1) NOT NULL
	) ON [PRIMARY]

*/
-- ====================================================================

create PROCEDURE [dbo].[VI_COMPENSA_MENSUAL]
  @felimite date
AS

BEGIN
  --
  ------------------------------------------------
  --Extrae para su tratamiento todo articulo que no sea importado, posea costo y pertenezca a algun grupo existente en
  --GRUPOSACRUZAR, seleccionando aquellos con stock negativo a la fecha informada y GRUPOSACRUZAR.sinegopos='N'
  --y tambien aquellos con stock positivo a la fecha informada y GRUPOSACRUZAR.sinegopos='P'
  --Nota: 1:15  ZHOG :: ZHOG, ZMOD, ZBIJ
  ------------------------------------------------
  IF OBJECT_ID('tempdb..#extraccion ') IS NOT NULL          
	DROP TABLE #extraccion
  IF OBJECT_ID('tempdb..#emparentados ') IS NOT NULL          
	DROP TABLE #emparentados
  IF OBJECT_ID('tempdb..#soloesos ') IS NOT NULL          
	DROP TABLE #soloesos
  IF OBJECT_ID('tempdb..#tratoeste ') IS NOT NULL          
	DROP TABLE #tratoeste

  SELECT p.CODIGO_PRODUCTO,
    P.GRUPO, P.DESCRIPCION,
    0 as marca,
    ISNULL(ff.PRECIO, isnull(P.COSTOUCP,0)) as PRECIO,
    isnull(ff.STOCK_INICIAL,0) as STOCK_INICIAL,
    isnull(ff.STOCK_ACTUAL,0) as STOCK_ACTUAL,
    isnull(tt.Porcentaje,0) as Porcentaje,
    isnull(ISNULL(ff.PRECIO, isnull(P.COSTOUCP,0))*(1-(tt.Porcentaje/100)),0) as premin,
    isnull(ISNULL(ff.PRECIO, isnull(P.COSTOUCP,0))*(1+(tt.Porcentaje/100)),0) as premax,
    ff.contador
  into #extraccion
  from productos p  
	outer APPLY (SELECT TOP 1
      f.STOCK_INICIAL, f.STOCK_ACTUAL, f.PRECIO, f.contador
    FROM FICHA_PRODUCTO f
    WHERE f.CODIGO_PRODUCTO=P.CODIGO_PRODUCTO and f.fechadoc<=@felimite
    order by f.fechadoc DESC, f.contador desc, f.falta desc) ff
	outer APPLY (SELECT TOP 1
      isnull(t.Porcentaje,0) as Porcentaje
    FROM SUSTITUCIONES_PORCENTAJES t
    WHERE ISNULL(ff.PRECIO, isnull(P.COSTOUCP,0)) between t.IMPORTE_DESDE and
	t.IMPORTE_HASTA) tt
  where isnull(P.Importado,'')<>'I' and ISNULL(ff.PRECIO, isnull(P.COSTOUCP,0))>0 and
    ((p.GRUPO = (select elgrup
    from GRUPOSACRUZAR
    where sinegopos='N') AND
    isnull(ff.STOCK_ACTUAL,0)<0) or
    (p.GRUPO in (select elgrup
    from GRUPOSACRUZAR
    where sinegopos='P') AND
    isnull(ff.STOCK_ACTUAL,0)>0))
  order by p.GRUPO,ISNULL(ff.PRECIO, isnull(P.COSTOUCP,0)),p.CODIGO_PRODUCTO
  --------------------------------------------------------------
  SELECT ROW_NUMBER() OVER(ORDER BY s.CODIGO_PRODUCTO) as fila,
    e.STOCK_ACTUAL+s.STOCK_ACTUAL as dife, 00 as marca,
    s.CODIGO_PRODUCTO, s.STOCK_ACTUAL, s.PRECIO, s.Porcentaje, s.premin, s.premax, s.grupo,
    e.CODIGO_PRODUCTO as CODIGO_PRODUCTOe, e.STOCK_ACTUAL as STOCK_ACTUALe, e.PRECIO as PRECIOe,
    e.Porcentaje as Porcentajee, e.premin as premine, e.premax as premaxe, e.grupo as grupoe,
    e.contador as contadore
  INTO #emparentados
  FROM #extraccion AS s, #extraccion e
  WHERE s.STOCK_ACTUAL<0 and e.STOCK_ACTUAL>0 and e.PRECIO between s.premin and s.premax
  order by s.CODIGO_PRODUCTO, e.STOCK_ACTUAL-s.STOCK_ACTUAL desc
  -------------------------------------------
  --delete #emparentados where CODIGO_PRODUCTO='400684' and STOCK_ACTUALe>16 --permite forzar a que aplique en partes (hasta 3)
  ------------------------------------------- hasta tres veces
  declare @veces int = 3
  WHILE @veces >0 and EXISTS (SELECT *
    from #extraccion
    where stock_actual<0)
	--and CODIGO_PRODUCTO in ('400684','401144','401798'))  para prueba
	BEGIN
    -- INICIO WHILE 
    set @veces = @veces -1
    IF OBJECT_ID('tempdb..#soloesos ') IS NOT NULL          
		DROP TABLE #soloesos
    select CODIGO_PRODUCTO, STOCK_ACTUAL, contador, PRECIO, Porcentaje, premin, premax, grupo
    into #soloesos
    from #extraccion
    where stock_actual<0
    --and CODIGO_PRODUCTO in ('400684','401144','401798') --para prueba
    order by CODIGO_PRODUCTO

    DECLARE @CODIGO_PRODUCTO varchaR(18), @fila int, @contadore int,
		@dife int, @STOCK_ACTUAL numeric(18), @PRECIO numeric(18,2), @Porcentaje numeric(18,2),
		@premin numeric(18,2), @premax numeric(18,2), @grupo nvarchar(4),
		@CODIGO_PRODUCTOe varchaR(18), @STOCK_ACTUALe numeric(18), @PRECIOe  numeric(18,2),
		@Porcentajee  numeric(18), @premine  numeric(18,2), @premaxe  numeric(18,2), @grupoe nvarchar(4)

    DECLARE stk_cursor CURSOR FOR
		select CODIGO_PRODUCTO, STOCK_ACTUAL, PRECIO, Porcentaje, premin, premax, grupo
    FROM #soloesos
    order by CODIGO_PRODUCTO
    OPEN stk_cursor
    FETCH NEXT FROM stk_cursor
		into @CODIGO_PRODUCTO, @STOCK_ACTUAL, @PRECIO, @Porcentaje, @premin, @premax, @grupo
    WHILE @@FETCH_STATUS = 0    
		BEGIN
      -- INICIO WHILE CURSOR
      IF OBJECT_ID('tempdb..#tratoeste ') IS NOT NULL          
				DROP TABLE #tratoeste

      select h.CODIGO_PRODUCTO, h.STOCK_ACTUAL, cc.CODIGO_PRODUCTOe, cc.STOCK_ACTUALe, cc.contadore,
        cc.PRECIO, cc.Porcentaje, cc.premin, cc.premax, cc.grupo, cc.dife
      INTO #tratoeste
      FROM #emparentados h
			OUTER APPLY (select top 1
          *
        from
          (                        SELECT TOP 1
              c.PRECIO, c.STOCK_ACTUAL, c.premin, c.premax, c.grupo, c.Porcentaje,
              c.contadore, c.STOCK_ACTUALe,
              '1' as orden, ABS(c.STOCK_ACTUALe + c.STOCK_ACTUAL) as dife, c.CODIGO_PRODUCTOe
            FROM #emparentados c
            WHERE CODIGO_PRODUCTO=h.CODIGO_PRODUCTO and ABS(c.STOCK_ACTUAL) <= c.STOCK_ACTUALe and
              c.contadore>0
            ORDER BY (ABS(c.STOCK_ACTUAL) - c.STOCK_ACTUALe) DESC
          UNION ALL
            SELECT TOP 1
              c.PRECIO, c.STOCK_ACTUAL, c.premin, c.premax, c.grupo, c.Porcentaje,
              c.contadore, c.STOCK_ACTUALe,
              '2' as orden, ABS(c.STOCK_ACTUALe + c.STOCK_ACTUAL) as dife, c.CODIGO_PRODUCTOe
            FROM #emparentados c
            where CODIGO_PRODUCTO=h.CODIGO_PRODUCTO and ABS(c.STOCK_ACTUAL) > c.STOCK_ACTUALe
            order by (ABS(c.STOCK_ACTUAL) - c.STOCK_ACTUALe) asc ) kk
        order by orden, dife ) cc
      where CODIGO_PRODUCTO= @CODIGO_PRODUCTO
      group by h.CODIGO_PRODUCTO, cc.CODIGO_PRODUCTOe, cc.PRECIO, h.STOCK_ACTUAL, cc.STOCK_ACTUALe, cc.premin,
				cc.premax, cc.grupo, cc.Porcentaje, cc.contadore, cc.dife
      order by h.CODIGO_PRODUCTO
      ------------------------hasta aqui rutina gral
      IF @@ROWCOUNT > 0
			begin
        set @contadore =  (select distinct contadore
        from #tratoeste)
        set @CODIGO_PRODUCTOe = (select distinct CODIGO_PRODUCTOe
        from #tratoeste)
        set @STOCK_ACTUALe = (select STOCK_ACTUALe
        from #tratoeste
        where contadore=@contadore)

        if (@STOCK_ACTUALe + @STOCK_ACTUAL)>=0 -- alcanza y/o sobra
			begin
          --select 'aqui estoy',  @CODIGO_PRODUCTO, @STOCK_ACTUAL, @PRECIO, @Porcentaje,
          -- @premin, @premax, @grupo, @CODIGO_PRODUCTOe, @STOCK_ACTUALe, @contadore  
          --select * from stock
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTO or CODIGO_PRODUCTO=@CODIGO_PRODUCTOe
          update stock set stock=stock-@STOCK_ACTUAL where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
          update stock set stock=stock+@STOCK_ACTUAL where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe
          --select * from stock where
          -- CODIGO_PRODUCTO=@CODIGO_PRODUCTO or CODIGO_PRODUCTO=@CODIGO_PRODUCTOe --ojo
          --select 'antes el neg', * from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTO order by FECHADOC, contador --ojo
          insert into FICHA_PRODUCTO
            (CODIGO_PRODUCTO,STOCK_INICIAL,STOCK_ACTUAL,FALTA,FECHADOC,NRODOC,TIPOMOV,CANTIDAD,
            PRECIO,PEDIDO,PROD_COMPENSA,PEDIDOID,ZONA,AnioCampania)
          VALUES
            (@CODIGO_PRODUCTO, @STOCK_ACTUAL, 0,
              @felimite, @felimite,
              '0', 'ID', @STOCK_ACTUAL*-1, @PRECIO, '0', @CODIGO_PRODUCTOe, 0, '   ', '      ')

          update FICHA_PRODUCTO
				set STOCK_INICIAL=STOCK_INICIAL-@STOCK_ACTUAL,
				STOCK_ACTUAL=STOCK_ACTUAL-@STOCK_ACTUAL
				where CODIGO_PRODUCTO=@CODIGO_PRODUCTO and fechadoc>@felimite
          --select 'despues el neg',* from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTO order by FECHADOC, contador --ojo
          ----------------------------
          --select 'antes el pos', * from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe order by FECHADOC, contador --ojo
          insert into FICHA_PRODUCTO
            (CODIGO_PRODUCTO,STOCK_INICIAL,STOCK_ACTUAL,FALTA,FECHADOC,NRODOC,TIPOMOV,CANTIDAD,
            PRECIO,PEDIDO,PROD_COMPENSA,PEDIDOID,ZONA,AnioCampania)
          VALUES
            (@CODIGO_PRODUCTOe, @STOCK_ACTUALe, @STOCK_ACTUALe+@STOCK_ACTUAL,
              @felimite, @felimite,
              '0', 'VD', @STOCK_ACTUAL*-1, @PRECIOe, '0', @CODIGO_PRODUCTO, 0, '   ', '      ')

          update FICHA_PRODUCTO
				set STOCK_INICIAL=STOCK_INICIAL+@STOCK_ACTUAL,
				STOCK_ACTUAL=STOCK_ACTUAL+@STOCK_ACTUAL
				where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe and fechadoc>@felimite
          --select 'despues el pos', * from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe order by FECHADOC, contador --ojo

          --finalmente actualizo los temporales
          if (select STOCK_ACTUALe + @STOCK_ACTUAL
          from #emparentados
          where CODIGO_PRODUCTO=@CODIGO_PRODUCTO and contadore=@contadore)>0
				begin
            update #emparentados set STOCK_ACTUAL = STOCK_ACTUAL + @STOCK_ACTUALe
						where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
            -- el negativo
            update #emparentados set STOCK_ACTUALe = STOCK_ACTUALe + @STOCK_ACTUAL
						where CODIGO_PRODUCTOe=@CODIGO_PRODUCTOe and contadore=@contadore

            update #extraccion set STOCK_ACTUAL = STOCK_ACTUAL - @STOCK_ACTUAL
						where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
          -- el negativo (acanzo)
          end
				else
				begin
            update #emparentados set STOCK_ACTUAL = STOCK_ACTUAL + @STOCK_ACTUALe
						where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
            -- el negativo
            update #emparentados set STOCK_ACTUALe = STOCK_ACTUALe + @STOCK_ACTUAL, contadore = 0
						where CODIGO_PRODUCTOe=@CODIGO_PRODUCTOe and contadore=@contadore

            update #extraccion set STOCK_ACTUAL = STOCK_ACTUAL + @STOCK_ACTUALe
						where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
          -- el negativo (no alcanzo)
          end
        end -- alcanza el stock del que elegi
			else -- Aqui deberia haber un END
			begin
          --select 'no alcanza',  @CODIGO_PRODUCTO, @STOCK_ACTUAL, @PRECIO, @Porcentaje,
          -- @premin, @premax, @grupo, @contadore, @CODIGO_PRODUCTOe, @STOCK_ACTUALe  --ojo
          --select * from stock
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTO or CODIGO_PRODUCTO=@CODIGO_PRODUCTOe --ojo

          update stock set stock=stock+@STOCK_ACTUALe where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
          update stock set stock=stock-@STOCK_ACTUALe where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe

          --select * from stock where
          -- CODIGO_PRODUCTO=@CODIGO_PRODUCTO or CODIGO_PRODUCTO=@CODIGO_PRODUCTOe --ojo
          --select 'antes el neg', * from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTO order by FECHADOC, contador --ojo

          insert into FICHA_PRODUCTO
            (CODIGO_PRODUCTO,STOCK_INICIAL,STOCK_ACTUAL,FALTA,FECHADOC,NRODOC,TIPOMOV,CANTIDAD,
            PRECIO,PEDIDO,PROD_COMPENSA,PEDIDOID,ZONA,AnioCampania)
          VALUES
            (@CODIGO_PRODUCTO, @STOCK_ACTUAL, @STOCK_ACTUAL+@STOCK_ACTUALe,
              @felimite, @felimite,
              '0', 'ID', @STOCK_ACTUALe, @PRECIO, '0', @CODIGO_PRODUCTOe, 0, '   ', '      ')

          update FICHA_PRODUCTO
			set STOCK_INICIAL=STOCK_INICIAL+@STOCK_ACTUALe,
			STOCK_ACTUAL=STOCK_ACTUAL+@STOCK_ACTUALe
			where CODIGO_PRODUCTO=@CODIGO_PRODUCTO and fechadoc>@felimite

          --select 'despues el neg',* from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTO order by FECHADOC
          --select 'antes el pos', * from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe order by FECHADOC, contador

          insert into FICHA_PRODUCTO
            (CODIGO_PRODUCTO,STOCK_INICIAL,STOCK_ACTUAL,FALTA,FECHADOC,NRODOC,TIPOMOV,CANTIDAD,
            PRECIO,PEDIDO,PROD_COMPENSA,PEDIDOID,ZONA,AnioCampania)
          VALUES
            (@CODIGO_PRODUCTOe, @STOCK_ACTUALe, 0,
              @felimite, @felimite,
              '0', 'VD', @STOCK_ACTUALe, @PRECIOe, '0', @CODIGO_PRODUCTO, 0, '   ', '      ')

          update FICHA_PRODUCTO
			set STOCK_INICIAL=STOCK_INICIAL-@STOCK_ACTUALe,
			STOCK_ACTUAL=STOCK_ACTUAL-@STOCK_ACTUALe
			where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe and fechadoc>@felimite

          --select 'despues el pos', * from FICHA_PRODUCTO
          -- where CODIGO_PRODUCTO=@CODIGO_PRODUCTOe order by FECHADOC, contador

          --finalmente actualizo los temporales
          if (select STOCK_ACTUALe - @STOCK_ACTUALe
          from #emparentados
          where CODIGO_PRODUCTO=@CODIGO_PRODUCTO and contadore=@contadore)>0
			begin
            update #emparentados set STOCK_ACTUAL = STOCK_ACTUAL + @STOCK_ACTUALe
				where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
            update #emparentados set STOCK_ACTUALe = STOCK_ACTUALe - @STOCK_ACTUALe
				where contadore=@contadore

            update #extraccion set STOCK_ACTUAL = STOCK_ACTUAL - @STOCK_ACTUAL
				where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
          -- el negativo (alcanzo)
          end
			else
			begin
            update #emparentados set STOCK_ACTUAL = STOCK_ACTUAL + @STOCK_ACTUALe
					where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
            update #emparentados set contadore = 0, STOCK_ACTUALe = 0
					where contadore=@contadore

            update #extraccion set STOCK_ACTUAL = STOCK_ACTUAL + @STOCK_ACTUALe
					where CODIGO_PRODUCTO=@CODIGO_PRODUCTO
          -- el negativo (no alcanzo)
          end
        end
      END
      -- no trajo #tratoeste

      FETCH NEXT FROM stk_cursor
			into @CODIGO_PRODUCTO, @STOCK_ACTUAL, @PRECIO, @Porcentaje, @premin, @premax, @grupo
    END
    -- END WHILE CURSOR
    CLOSE stk_cursor
    DEALLOCATE stk_cursor
  end
-- END WHILE
END
GO
