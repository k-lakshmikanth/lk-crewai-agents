from crewai import Agent, Crew, Process, Task

sp_pc_agt = Agent(
    role="SQL Stored Procedure Analyst",
    goal="Accurately convert SQL Stored Procedures into structured and understandable pseudocode converting it into any user defined function.",
    backstory="""With years of experience in enterprise database design and SQL performance tuning, you specialize in dissecting and simplifying complex stored procedures.
    Your work helps developers and architects understand the logic behind stored procedures without needing to dig into database-specific syntax.
    You are meticulous, clear in your documentation, and ensure that each pseudocode output can be confidently implemented or refactored by any developer(no programming language barrier).
"""
)

sp_pc_tsk = Task(
    description="""Your task is to analyze the given SQL Stored Procedure (SP) and rewrite it as clear, structured pseudo code.
    The goal is to produce an understandable representation of the procedure’s logic for documentation or refactoring purposes.

    The pseudo code must:
    - Clearly define the procedure name and input parameters
    - Translate SQL control flow (IF/ELSE, WHILE, CASE, etc.) into pseudo code logic
    - Avoid actual SQL execution; focus on logical flow
    - Include comments (prefixed with "--") to explain what each section does
    - Declare any variables or intermediate steps clearly
    - Follow SQL-style formatting with capitalized keywords for clarity

    SQL Stored Procedure:
    {stored_procedure}
""",
    agent=sp_pc_agt,
    expected_output="<pure pseudo code>"
)

crew = Crew(
    agents=[sp_pc_agt],
    tasks=[sp_pc_tsk]
)

sp = """CREATE PROCEDURE [dbo].[uspLogError]
    @ErrorLogID int = 0 OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET @ErrorLogID = 0;

    BEGIN TRY
        IF ERROR_NUMBER() IS NULL
            RETURN;

        IF XACT_STATE() = -1
        BEGIN
            PRINT 'Cannot log error since the current transaction is in an uncommittable state. '
                + 'Rollback the transaction before executing uspLogError in order to successfully log error information.';
            RETURN;
        END

        INSERT [dbo].[ErrorLog]
            (
            [UserName],
            [ErrorNumber],
            [ErrorSeverity],
            [ErrorState],
            [ErrorProcedure],
            [ErrorLine],
            [ErrorMessage]
            )
        VALUES
            (
            CONVERT(sysname, CURRENT_USER),
            ERROR_NUMBER(),
            ERROR_SEVERITY(),
            ERROR_STATE(),
            ERROR_PROCEDURE(),
            ERROR_LINE(),
            ERROR_MESSAGE()
            );

        SET @ErrorLogID = @@IDENTITY;
    END TRY
    BEGIN CATCH
        PRINT 'An error occurred in stored procedure uspLogError: ';
        EXECUTE [dbo].[uspPrintError];
        RETURN -1;
    END CATCH
END;
"""

inputs = {
    "stored_procedure":sp
}

res = crew.kickoff(inputs=inputs)

print(res)