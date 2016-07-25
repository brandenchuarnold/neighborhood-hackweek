
IF OBJECT_ID('dbo.pkRegionData') IS NOT NULL
BEGIN
    PRINT 'Dropping constraint pkRegionData';

    ALTER TABLE dbo.RegionData
    DROP CONSTRAINT pkRegionData;
END;

PRINT 'Creating constraint pkRegionData';

ALTER TABLE dbo.RegionData
ADD CONSTRAINT pkRegionData
PRIMARY KEY CLUSTERED (
    RegionID
);
