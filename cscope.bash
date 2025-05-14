function gen_cscopefiles()
{
    rm temp_cscope.txt
		find . -name "*.elf" -exec llvm-dwarfdump --show-sources {} + | sort | uniq >> temp_cscope.txt
        sed -i '/^$/d' temp_cscope.txt
        sed -i 's/"//g' temp_cscope.txt
        cscope -i temp_cscope.txt -Rbk
        rm temp_cscope.txt
}

