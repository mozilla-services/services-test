for /f %%i in ('qwinsta ^| findstr /C:">rdp-tcp#"') do set RDP_SESSION=%%i
:: Strip the >
set RDP_SESSION=%RDP_SESSION:>=%
echo "NEW RDP SESSION: %RDP_SESSION%"
tscon %RDP_SESSION% /dest:consolea
