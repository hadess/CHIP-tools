#! /bin/bash

SPL=$1
UBOOT=$2
KERNEL=$3
DTB=$4
INITRD=$5
SCRIPT=$6
FEL=$(get_fel)
if [ $? != 0 ] ; then
  echo "fel is missing"
  exit 1
fi

echo == upload the SPL to SRAM and execute it ==
${FEL} spl $SPL

sleep 1 # wait for DRAM initialization to complete

echo == upload the main u-boot binary to DRAM ==
${FEL} write 0x4a000000 $UBOOT

echo == upload the kernel ==
${FEL} write 0x42000000 $KERNEL

echo == upload the DTB file ==
${FEL} write 0x43000000 $DTB

echo == upload the boot.scr file ==
${FEL} write 0x43100000 $SCRIPT

echo == upload the initramfs file ==
${FEL} write 0x43300000 $INITRD

echo == execute the main u-boot binary ==
${FEL} exe   0x4a000000
