/*---------------------------------------------------------------------------------------
Cache of RegionData for a RegionID (must be a neighborhood)

Change History:
    Date        Author          Description
    ----------  --------------- -----------------------------
    2016-07-12  brandena        created
---------------------------------------------------------------------------------------*/
IF OBJECT_ID(N'dbo.RegionData') IS NULL
BEGIN
    PRINT 'Creating table RegionData'
    CREATE TABLE dbo.RegionData
    (
        RegionID                          INTEGER NOT NULL,
        MedianMonthlyIncome               MONEY NULL,
        MeanHouseHoldSize                 DECIMAL(5, 2) NULL,
        MeanMinBed                        DECIMAL(5, 2) NULL,
        MeanMaxBed                        DECIMAL(5, 2) NULL,
        PercentCreditScoreOver700         DECIMAL(5, 4) NULL,
        PercentOwnCurrentHome             DECIMAL(5, 4) NULL,
        PercentFlexibleMoveInDate         DECIMAL(5, 4) NULL,
        PercentLongTermLease              DECIMAL(5, 4) NULL,
        PercentMoreThanOneBed             DECIMAL(5, 4) NULL,
        PercentNeedParking                DECIMAL(5, 4) NULL
    )
END
GO
