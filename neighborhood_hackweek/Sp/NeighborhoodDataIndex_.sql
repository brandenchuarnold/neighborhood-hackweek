IF OBJECT_ID('dbo.NeighborhoodDataIndex_') IS NULL
    BEGIN
        EXEC('CREATE PROCEDURE dbo.NeighborhoodDataIndex_ AS RETURN 0')
    END
GO

PRINT 'Altering stored procedure NeighborhoodDataIndex_'
GO

ALTER PROCEDURE dbo.NeighborhoodDataIndex_
AS

/*-----------------------------------------------------------------------------
Description
    Indexes a set of region data
    Requires NeighborhoodDataToIndex to be populated

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
    @NOW                                    smalldatetime,
	@N										int

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

INSERT INTO [RegionData]
SELECT RegionID,
    (
        (SELECT MAX(MonthlyIncomeAmt) FROM
            (SELECT TOP 50 PERCENT MonthlyIncomeAmt
			 FROM #NeighborhoodDataToIndex
             WHERE MonthlyIncomeAmt IS NOT NULL
			 ORDER BY MonthlyIncomeAmt) AS BottomHalf)
        +
        (SELECT MIN(MonthlyIncomeAmt) FROM
            (SELECT TOP 50 PERCENT MonthlyIncomeAmt
			 FROM #NeighborhoodDataToIndex
             WHERE MonthlyIncomeAmt IS NOT NULL
			 ORDER BY MonthlyIncomeAmt DESC) AS TopHalf)
	/ 2) AS MedianMonthlyIncome,
    AVG(HouseholdSizeCnt) AS MeanHouseHoldSize,
    AVG(BedroomCntMin) AS MeanMinBed,
    AVG(BedroomCntMax) AS MeanMaxBed,
    SUM(CASE WHEN CreditScoreTypeID >= 3 THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(CreditScoreTypeID) FROM #NeighborhoodDataToIndex) AS PercentCreditScoreOver700,
    SUM(CASE WHEN HousingTypeCurrentName = 'own' THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(HousingTypeCurrentName) FROM #NeighborhoodDataToIndex) AS PercentOwnCurrentHome,
    SUM(CASE WHEN MoveInPeriodTypeName = 'I''m flexible' THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(MoveInPeriodTypeName) FROM #NeighborhoodDataToIndex) AS PercentFlexibleMoveInDate,
    SUM(CASE WHEN LeaseDurationTypeName = 'long (12+ months)' THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(LeaseDurationTypeName) FROM #NeighborhoodDataToIndex) AS PercentLongTermLease,
    SUM(CASE WHEN BedroomCntMin > 1 THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(BedroomCntMin) FROM #NeighborhoodDataToIndex) AS PercentMoreThanOneBed,
    SUM(CASE WHEN ParkingNeedTypeName = 'yes' THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(ParkingNeedTypeName) FROM #NeighborhoodDataToIndex) AS PercentNeedParking,
    (SELECT COUNT(*) FROM #RentalPropertyContacted)) * 1.0 / (SELECT COUNT(*) FROM #RentalPropertyAll) AS NumContactsPerRental,
	(SELECT CurrentDataValue from #Zindex) AS Zindex
FROM #NeighborhoodDataToIndex
GROUP BY RegionID

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

GRANT EXECUTE ON dbo.NeighborhoodDataIndex_ TO ProdUser
*/
