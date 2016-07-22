IF OBJECT_ID('dbo.PropertyRegionLst_') IS NULL
    BEGIN
        EXEC('CREATE PROCEDURE dbo.PropertyRegionLst_ AS RETURN 0')
    END
GO

PRINT 'Altering stored procedure PropertyRegionLst_'
GO

ALTER PROCEDURE dbo.PropertyRegionLst_
AS

/*-----------------------------------------------------------------------------
Description
    This sproc requires that it is called from another sproc (e.g. PropertyRegionLst)
    AND that the calling sproc populate table #PropertyRegionToReturn

Result sets

Return values
    0     Success
    -100  Failure

Error codes
    200001  Parameter error
    200100  SP: %s. Unexpected error. See previous error messages. Error number: %d.'
    200300  Error inserting data into %s

Change History
    Date        Author          Description
    ----------  --------------- ----------------------------------------------
    2016-07-13  brandena        Created
-----------------------------------------------------------------------------*/
SET NOCOUNT ON
IF (@@trancount = 0)
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


DECLARE  -- Standard constants and variables
    @RC_FAILURE                             int,
    @RC_SUCCESS                             int,
    @SUCCESS                                int,
    @ErrNum                                 int,
    @ExitCode                               int,
    @ProcedureName                          sysname,
    @RowCnt                                 int,

-- Error message constants and variables
    @ERR_PARAMETER                          int,
    @ERR_UNEXPECTED                         int,
    @ERR_UPDATE                             int,
    @MsgParm1                               varchar(100),

-- Procedure-specific constants and variables
    @NOW                                    smalldatetime

-- Standard constants
SET @RC_FAILURE                             = -100
SET @RC_SUCCESS                             = 0
SET @SUCCESS                                = 0

-- Standard variables
SET @ExitCode                               = @RC_SUCCESS
SET @ProcedureName                          = OBJECT_NAME( @@PROCID )

-- Error message constants
SET @ERR_PARAMETER                          = 200001
SET @ERR_UNEXPECTED                         = 200100
SET @ERR_UPDATE                             = 200310

-- Procedure-specific constants and variables
SET @NOW                                    = GETDATE()

SELECT
    orig.PropertyID,
    orig.RegionIdNeighborhood,
    pu.SellingPriceDollarCnt,
	rz.ZestimateDollarCnt,
	pt.TaxPaidAmt,
	pa.Bedrooms,
	pa.Bathrooms,
	pll.Latitude,
	pll.Longitude
FROM #PropertyRegionToReturn tr
JOIN dbo.PropertyRegion orig
    ON tr.PropertyID = orig.PropertyID
    AND tr.DataSourceTypeID = orig.DataSourceTypeID
JOIN User_tes_600_comp_ads.dbo.PostingUnion pu
    ON tr.PostingID = pu.PostingID
JOIN RentalZestimate_tes_600_comp_ads.dbo.RentalZestimateCurrent rz
	ON tr.PropertyID = rz.PropertyID
JOIN dbo.PropertyTax pt
	ON tr.PropertyID = pt.PropertyID
	AND tr.DataSourceTypeID = pt.DataSourceTypeID
	AND pt.BestRecordFlag = 1
JOIN dbo.PropertyAttribute pa
	ON tr.PropertyID = pa.PropertyID
	AND tr.DataSourceTypeID = pa.DataSourceTypeID
	AND pa.BestRecordFlag = 1
JOIN dbo.PropertyLatLong pll
	ON tr.PropertyID = pll.PropertyID
	AND tr.DataSourceTypeID = pll.DataSourceTypeID
	AND pll.BestRecordFlag = 1

GOTO ExitProc

-------------------------------------------------------------------------------
-- Error Handler
-------------------------------------------------------------------------------
ErrorHandler:
    SET @ExitCode = @RC_FAILURE
    GOTO ExitProc

-------------------------------------------------------------------------------
-- Exit Procedure
-------------------------------------------------------------------------------
ExitProc:
    RETURN (@ExitCode)
GO


/* Test by running PropertyRegionLst

GRANT EXECUTE ON dbo.PropertyRegionLst_ TO ProdUser
*/
