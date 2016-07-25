IF OBJECT_ID('dbo.NeighborhoodDataGetByRegionIDNeighborhood') IS NULL
    BEGIN
        EXEC('CREATE PROCEDURE dbo.NeighborhoodDataGetByRegionIDNeighborhood AS RETURN 0')
    END
GO

PRINT 'Altering stored procedure NeighborhoodDataGetByRegionIDNeighborhood'
GO

ALTER PROCEDURE dbo.NeighborhoodDataGetByRegionIDNeighborhood
(
    @pRegionIDNeighborhood        int
)
AS

/*-----------------------------------------------------------------------------
Description
   Gets Neighborhood data based on a region id for a neighborhood 

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

IF ((SELECT COUNT(1) FROM dbo.RegionData WHERE RegionID = @pRegionIDNeighborhood) = 0)
	BEGIN
		EXEC @RC = NeighborhoodDataIndexByRegionIDNeighborhood @pRegionIDNeighborhood
	END

SELECT *
FROM dbo.RegionData
WHERE RegionID = @pRegionIDNeighborhood

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
GRANT EXECUTE ON dbo.NeighborhoodDataGetByRegionIDNeighborhood TO ProdUser
*/