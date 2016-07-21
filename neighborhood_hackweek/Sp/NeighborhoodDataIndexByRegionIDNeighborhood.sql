IF OBJECT_ID('dbo.NeighborhoodDataIndexByRegionIDNeighborhood') IS NULL
    BEGIN
        EXEC('CREATE PROCEDURE dbo.NeighborhoodDataIndexByRegionIDNeighborhood AS RETURN 0')
    END
GO

PRINT 'Altering stored procedure NeighborhoodDataIndexByRegionIDNeighborhood'
GO

ALTER PROCEDURE dbo.NeighborhoodDataIndexByRegionIDNeighborhood
(
    @pRegionIDNeighborhood        int
)
AS

/*-----------------------------------------------------------------------------
Description
   Indexes Neighborhood data based on a region id for a neighborhood 

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
    2016-07-18  brandena        created
-----------------------------------------------------------------------------*/
SET NOCOUNT ON
IF (@@trancount = 0)
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED

DECLARE  -- Standard constants and variables
    @RC                                     int,
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
    @MsgParm1                               varchar(100)

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


-- Make sure none of these input variables have been set to NULL.
SET @MsgParm1 = CASE
        WHEN @pRegionIDNeighborhood            IS NULL THEN '@pRegionIDNeighborhood'
        ELSE NULL
    END

IF @MsgParm1 IS NOT NULL
    BEGIN
        RAISERROR( @ERR_PARAMETER, 16, -1, @ProcedureName, @MsgParm1, 'NULL' )
        GOTO ErrorHandler
    END

-- Temporary tables
CREATE TABLE #NeighborhoodDataToIndex
(
    AccountID				integer not null,
	PostalCodeFrom			varchar(10) null,
	HousingSinceDate		date null,
	HousingTypeCurrentName		varchar(60) null,
	EmployedSinceDate		date null,
	CreditScoreTypeID		tinyint null,
	MonthlyIncomeAmt		int null,
	HousingTypeDesiredName		varchar(60) null,
	MoveInPeriodTypeName		varchar(60) null,
	LeaseDurationTypeName		varchar(60) null,
	HouseholdSizeCnt		tinyint null,
	BedroomCntMin			tinyint null,
	BedroomCntMax			tinyint null,
	ParkingNeedTypeName		varchar(60) null,
	CreateDate			datetime2(0) null,
	RegionID			integer not null
)
------------------------------------------------------------------------------
-- Processing
------------------------------------------------------------------------------
INSERT INTO #NeighborhoodDataToIndex
SELECT rres.AccountID,
	  rres.PostalCodeFrom,
	  rres.HousingSinceDate,
	  rhousecurr.HousingTypeCurrentName,
	  rres.EmployedSinceDate,
	  rres.CreditScoreTypeID, 
	  rres.MonthlyIncomeAmt,
	  rhousewant.HousingTypeDesiredName, 
	  movein.MoveInPeriodTypeName,  
	  leasedur.LeaseDurationTypeName,
	  rres.HouseholdSizeCnt, 
	  rres.BedroomCntMin,
	  rres.BedroomCntMax,
	  park.ParkingNeedTypeName,
	  rres.CreateDate,
	  rreg.RegionID
	  FROM [AccountRenterResume] AS rres
	  JOIN [AccountRenterResumeRegion] AS rreg
	  ON rres.AccountID = rreg.AccountID
	  LEFT JOIN [AccountRenterResumeHousingTypeDesired] AS rhousewantID
	  ON rres.AccountID = rhousewantID.AccountID
	  LEFT JOIN [HousingTypeDesired] AS rhousewant
	  ON rhousewantID.HousingTypeDesiredID = rhousewant.HousingTypeDesiredID
	  LEFT JOIN [HousingTypeCurrent] AS rhousecurr
	  ON rres.HousingTypeCurrentID = rhousecurr.HousingTypeCurrentID
	  LEFT JOIN [MoveInPeriodType] AS movein
	  ON rres.MoveInPeriodTypeID = movein.MoveInPeriodTypeID
	  LEFT JOIN [LeaseDurationType] AS leasedur
	  ON rres.LeaseDurationTypeID = leasedur.LeaseDurationTypeID
	  LEFT JOIN [ParkingNeedType] AS park
	  ON rres.ParkingNeedTypeID = park.ParkingNeedTypeID
	  WHERE rreg.RegionID = @pRegionIDNeighborhood
	  AND rreg.StatusTypeID = 1
	  AND rres.StatusTypeID = 1
	  AND rres.LastUpdateBy = 'renter-resume-service'
	  AND rhousewant.HousingTypeDesiredName != 'apartment'

EXEC @RC = NeighborhoodDataIndex_

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


/*
GRANT EXECUTE ON dbo.NeighborhoodDataIndexByRegionIDNeighborhood TO ProdUser
*/